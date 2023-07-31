from .adapters.base_adapter import BaseAdapter
from typing import Any, Dict, List, Optional


class CachePyramid:
    def __init__(self, adapters: List[BaseAdapter]) -> None:
        self.adapters: List[BaseAdapter] = adapters
        pass

    def getAdapters(self) -> List[BaseAdapter]:
        return self.adapters

    def setAdapters(self, adapters: List[BaseAdapter]) -> None:
        self.adapters = adapters

    def setAdapter(self, adapter: BaseAdapter, position: int) -> None:
        if position > len(self.adapters):
            raise IndexError
        if position == len(self.adapters):
            self.adapters.append(adapter)
        self.adapters[position] = adapter

    def get(self, key: str) -> Optional[Any]:
        for i, adapter in enumerate(self.adapters):
            result = adapter.get(key)
            if result is not None:
                # populate higher-level layers
                for higher_adapter in self.adapters[:i]:
                    higher_adapter.set(key, result)
                return result
        return None

    def mget(self, keys: List[str]) -> Dict[str, Optional[Any]]:
        result = {}
        remaining_keys = keys[:]
        highest_level_adapter_used = len(self.adapters)

        for i, adapter in enumerate(self.adapters):
            if not remaining_keys:
                highest_level_adapter_used = i
                break

            partial_result = adapter.mget(remaining_keys)
            for key, value in partial_result.items():
                if value is not None:
                    result[key] = value
                    remaining_keys.remove(key)
        if result:
            for higher_adapter in self.adapters[:highest_level_adapter_used]:
                higher_adapter.mset(result)

        return result

    def set(self, key: str, value: Any) -> None:
        for adapter in self.adapters:
            adapter.set(key, value)

    def mset(self, items: Dict[str, Any]) -> None:
        for adapter in self.adapters:
            adapter.mset(items)

    def delete(self, key: str) -> None:
        for adapter in self.adapters:
            adapter.delete(key)

    def exists(self, key: str) -> bool:
        for adapter in self.adapters:
            if adapter.exists(key):
                return True
        return False

    def flush(self) -> None:
        for adapter in self.adapters:
            adapter.flush()
