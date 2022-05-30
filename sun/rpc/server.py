import etcd3
import json


class RpcEtcdClient(etcd3.Etcd3Client):
    def get_values_by_key(self, key, **kwargs):
        values, _ = self.get(key, **kwargs)
        values_list = []
        if values is not None:
            try:
                values_list = json.loads(values.decode('utf-8'))
                if not isinstance(values_list, list):
                    raise TypeError()
            except:
                raise Exception()

        return values_list

    def put_values_by_key(self, key, values):
        if not isinstance(values, list):
            raise Exception()
        self.put(key, json.dumps(values).encode('utf-8'))

    def put_value_by_key(self, key, value):
        self.put(key, value)

    def get_value_by_key(self, key, **kwargs):
        value, _ = self.get(key, **kwargs)
        return value

    def del_value_by_key(self, key, **kwargs):
        self.delete(key, **kwargs)


class RpcHandleServer:
    def __init__(self, service_ip, service_port, service_key, etcd_ip, etcd_port):
        self.time_to_live = 10
        self.etcd_ip = etcd_ip
        self.etcd_port = etcd_port
        self.etcd_client = RpcEtcdClient(host=self.etcd_ip, port=self.etcd_port)
        lease = self.etcd_client.lease(self.time_to_live)

        self.service_key = service_key
        self.service_lease_id = lease.id

        self.endpoint = f'{service_ip}:{service_port}'

    def register_service(self):
        """"""
        key_name = f'{self.service_key}/{self.service_lease_id}'
        with self.etcd_client.lock(key_name):
            self.etcd_client.put_value_by_key(key_name, self.endpoint)

    def logout_service(self):
        """"""
        key_name = f'{self.service_key}/{self.service_lease_id}'
        with self.etcd_client.lock(key_name):
            self.etcd_client.del_value_by_key(key_name)
