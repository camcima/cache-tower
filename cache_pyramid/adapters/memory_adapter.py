from .base_adapter import BaseAdapter
from typing import Any, Dict, List, Optional


class MemoryAdapter(BaseAdapter):
    def __init__(self, params: dict = {}, namespace: str = "", ttl: int = 0) -> None:
        super().__init__(params, namespace, ttl)
        self.data: Dict[str, Any] = {}

    def get(self, key: str) -> Any:
        return self.data.get(self._create_key(key))

    def mget(self, keys: List[str]) -> Dict[str, Optional[Any]]:
        return {key: self.data.get(self._create_key(key)) for key in keys}

    def set(self, key: str, value: Any) -> None:
        self.data[self._create_key(key)] = value

    def mset(self, items: Dict[str, Any]) -> None:
        self.data.update(self._create_items(items))

    def delete(self, key: str) -> None:
        if self._create_key(key) in self.data:
            del self.data[self._create_key(key)]

    def exists(self, key: str) -> bool:
        return self._create_key(key) in self.data

    def flush(self) -> None:
        self.data = {}
