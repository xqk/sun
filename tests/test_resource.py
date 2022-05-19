from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from sun.db import db
from sun.db.operators import get_filters_expr
from sun.decorators import action
from sun.resources import Resource
from sun.schemas import ListRequest
from tests.main import IsAuthenticated

DB_URI = 'sqlite:///:memory:'

db.connect(DB_URI)


class User(db.BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), default='')
    age = Column(Integer)


# generate records
db.create_all()
lucy = User.create(**{
    'username': 'Lucy',
    'age': 13,
})
jack = User.create(**{
    'username': 'Jack',
    'age': 20,
})
groot = User.create(**{
    'username': 'Groot',
    'age': 32,
})


class UserSchema(BaseModel):
    id: int
    username: str
    age: int


class UserResource(Resource):

    schema = UserSchema
    filters = [
        {'username': str},
        {'age': Optional[str]},
    ]  # yapf: disable
    permission_classes = [IsAuthenticated]

    @action()
    def get(self, pk=None):
        return User.first(id=pk)

    @action()
    def list(self, schema_in: ListRequest = None):
        return User.query().filter(
            *get_filters_expr(User, **schema_in.filters)
        )

    @action()
    def create(self, schema_in: schema = None):
        return User.create(**schema_in.dict())

    @action()
    def update(self, schema_in: schema = None, pk=None):
        user = User.first(id=pk)
        for k, v in schema_in.dict().items():
            setattr(user, k, v)
        return user.save()

    @action()
    def delete(self, pk=None):
        User.delete(id=pk)
        return {'result': True}

    @action(detail=False)
    def recents(self):
        return User.query().all()[:2]


def test_resource_instance():
    resource = UserResource()
    assert hasattr(resource, 'as_router')
    assert resource._is_http
    assert not resource._is_rpc


def test_resource_generic_actions():
    resource = UserResource()
    get_result = resource.get(pk=1)
    assert get_result == User.first(id=1)


def test_resource_custom_actions():
    resource = UserResource()
    assert len(resource.recents()) > 0
