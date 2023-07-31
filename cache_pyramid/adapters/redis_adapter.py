from .base_adapter import BaseAdapter
from typing import Any, Dict, List, Optional
import redis


class RedisAdapter(BaseAdapter):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
    ):
        self.redis_client = redis.Redis(
            host=host, port=port, db=db, password=password, decode_responses=True
        )

    def get(self, key: str) -> Any:
        return self.redis_client.get(key)

    def mget(self, keys: List[str]) -> Dict[str, Optional[Any]]:
        values = self.redis_client.mget(keys)
        return dict(zip(keys, values))

    def set(self, key: str, value: Any) -> None:
        self.redis_client.set(key, value)

    def mset(self, items: Dict[str, Any]) -> None:
        self.redis_client.mset(items)

    def delete(self, key: str) -> None:
        self.redis_client.delete(key)

    def exists(self, key: str) -> bool:
        return bool(self.redis_client.exists(key))

    def flush(self) -> None:
        self.redis_client.flushdb()
