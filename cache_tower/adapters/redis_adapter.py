from .base_adapter import BaseAdapter
from typing import Any, Dict, List, Optional
import redis


class RedisAdapter(BaseAdapter):
    def __init__(self, params: dict, namespace: str = "", ttl: int = 0) -> None:
        super().__init__(params, namespace, ttl)
        self._redis_client = redis.Redis(**params)

    def get(self, key: str) -> Any:
        return self._redis_client.get(self._create_key(key))

    def mget(self, keys: List[str]) -> Dict[str, Optional[Any]]:
        values = self._redis_client.mget(self._create_keys(keys))
        return dict(zip(keys, values))

    def set(self, key: str, value: Any) -> None:
        self._redis_client.set(self._create_key(key), value, ex=self._ttl)

    def mset(self, items: Dict[str, Any]) -> None:
        self._redis_client.mset(self._create_items(items))  # type: ignore
        if self._ttl > 0:
            for key in items:
                self._redis_client.expire(self._create_key(key), self._ttl)

    def delete(self, key: str) -> None:
        self._redis_client.delete(self._create_key(key))

    def exists(self, key: str) -> bool:
        return bool(self._redis_client.exists(self._create_key(key)))

    def flush(self) -> None:
        self._redis_client.flushdb()
