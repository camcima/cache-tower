from http import client
from .base_adapter import BaseAdapter
from typing import Any, Dict, List, Optional
from pymemcache.client.base import Client, PooledClient
from pymemcache.client.hash import HashClient


class MemcachedAdapter(BaseAdapter):
    def __init__(self, params: dict, namespace: str = "", ttl: int = 0) -> None:
        super().__init__(params, namespace, ttl)
        memcached_params = params.copy()
        self._client_type = memcached_params.pop('client_type')
        if self._client_type == "client":
            self._memcached_client = Client(**memcached_params)
        elif self._client_type == "pooled_client":
            self._memcached_client = PooledClient(**memcached_params)
        elif self._client_type == "hash_client":
            self._memcached_client = HashClient(**memcached_params)
        else:
            raise RuntimeError("Invalid client type for the memcached adapter")

    def get(self, key: str) -> Any:
        return self._memcached_client.get(self._create_key(key))

    def mget(self, keys: List[str]) -> Dict[str, Optional[Any]]:
        values = self._memcached_client.get_multi(self._create_keys(keys))
        return dict(zip(keys, values))

    def set(self, key: str, value: Any) -> None:
        self._memcached_client.set(self._create_key(key), value, expire=self._ttl)

    def mset(self, items: Dict[str, Any]) -> None:
        self._memcached_client.set_multi(self._create_items(items), expire=self._ttl)

    def delete(self, key: str) -> None:
        self._memcached_client.delete(self._create_key(key))

    def exists(self, key: str) -> bool:
        return bool(self._memcached_client.get(self._create_key(key)))

    def flush(self) -> None:
        self._memcached_client.flush_all()
