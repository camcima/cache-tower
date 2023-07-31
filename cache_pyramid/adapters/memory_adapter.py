from .base_adapter import BaseAdapter
from typing import Any, Dict, List, Optional


class MemoryAdapter(BaseAdapter):
    def __init__(self) -> None:
        self.data: Dict[str, Any] = {}

    def get(self, key: str) -> Any:
        return self.data.get(key)

    def mget(self, keys: List[str]) -> Dict[str, Optional[Any]]:
        return {key: self.data.get(key) for key in keys}

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value

    def mset(self, items: Dict[str, Any]) -> None:
        self.data.update(items)

    def delete(self, key: str) -> None:
        if key in self.data:
            del self.data[key]

    def exists(self, key: str) -> bool:
        return key in self.data

    def flush(self) -> None:
        self.data = {}
