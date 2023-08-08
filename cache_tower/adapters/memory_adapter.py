import time
import threading
from .base_adapter import BaseAdapter
from typing import Any, Dict, List, Optional
from collections import OrderedDict


class MemoryAdapter(BaseAdapter):
    def __init__(self, params: dict = {}, namespace: str = "", ttl: int = 0) -> None:
        super().__init__(params, namespace, ttl)
        self._maxsize = params.get("maxsize", 0)
        self._lru = params.get("lru", False)
        self._lock = threading.RLock()
        self._data: OrderedDict = OrderedDict()

    def get(self, key: str) -> Any:
        with self._lock:
            value = self._data.get(self._create_key(key), None)
            if not value:
                return None
            if self._ttl > 0 and time.time() - value[0] > self._ttl:
                del self._data[self._create_key(key)]
                return None
            if self._lru:
                self._data.move_to_end(self._create_key(key))
            return value[1]

    def mget(self, keys: List[str]) -> Dict[str, Optional[Any]]:
        values = {}
        for key in keys:
            values[key] = self.get(key)
        return values

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            while self._maxsize > 0 and len(self._data) >= self._maxsize:
                self._data.popitem(last=False)
            self._data[self._create_key(key)] = (time.time(), value)

    def mset(self, items: Dict[str, Any]) -> None:
        for key, value in items.items():
            self.set(key, value)

    def delete(self, key: str) -> None:
        if self._create_key(key) in self._data:
            del self._data[self._create_key(key)]

    def exists(self, key: str) -> bool:
        return self._create_key(key) in self._data

    def flush(self) -> None:
        self._data = OrderedDict()
