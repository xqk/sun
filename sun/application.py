import gzip
import inspect
from multiprocessing import Process
from typing import Callable

import typer
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.routing import APIRoute
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from ._utils import singleton
from .middlewares import process_middleware
from .utils import sync_exec


class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body


class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler


@singleton
class Sun:
    def __init__(self, base_settings=None, **kwargs):
        self.base_settings = base_settings or {}
        self.kwargs = kwargs
        self._app = None

        self.http()  # Create FastAPI instance ref to `self._app`

    def __getattribute__(self, attr, *args, **kwargs):
        try:
            return super().__getattribute__(attr)
        except AttributeError:
            return getattr(self._app, attr)

    async def __call__(self, scope, receive, send) -> None:
        self.http()
        await self._app.__call__(scope, receive, send)  # pragma: no cover

    def _launch_http(self):
        self._app = FastAPI(**self.base_settings)
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            access_log=True
        )

    async def _launch_rpc(self):
        service = self.kwargs.get('rpc_service')
        if not service:
            raise Exception('rpc_service not provided')
        if inspect.iscoroutinefunction(service.serve):
            await service.serve()
        else:
            service.serve()

    def _launch_event(self):
        from .events import handle
        while True:
            handle()

    def _start_all(self):
        process_http = Process(target=self._launch_http)
        process_http.start()
        process_rpc = Process(target=self._launch_rpc)
        process_rpc.start()
        process_rpc.join()
        process_http.join()

    def settings(self, **kwargs):
        self.base_settings.update(kwargs)

    def http(self):
        """load FastAPI to instance"""
        self._app = FastAPI(**self.base_settings)
        self._app.router.route_class = GzipRoute

        # routers
        for router in self.kwargs.get('routers', []):
            self._app.include_router(**router)
        # cors
        backend_cors_origins = self.kwargs.get('backend_cors_origins')
        if backend_cors_origins:
            self._app.add_middleware(GZipMiddleware)
            self._app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in backend_cors_origins],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            self._app.middleware('http')(process_middleware)

        add_pagination(self._app)

    def launch(
        self, http: bool = False, rpc: bool = False, event: bool = False
    ):
        if not http and not rpc and not event:
            typer.echo(
                'Please provided launch service type: --http or --rpc or --event'
            )

        if http:
            self._launch_http()

        if rpc:
            sync_exec(self._launch_rpc())

        if event:
            self._launch_event()

    def start(self):
        typer.run(self.launch)
