import importlib
import string
from .adapters.base_adapter import BaseAdapter
from typing import Any, Dict, List, Optional


class CachePyramid:
    def __init__(self, config: List[dict]) -> None:
        self._config: List[dict] = config
        self._adapters: List[BaseAdapter] = []
        if self._config:
            self.__initialize_adapters()
        pass

    def __initialize_adapters(self) -> None:
        for adapter_config in self._config:
            self._adapters.append(self.__create_adapter(adapter_config))

    def __create_adapter(self, adapter_config: dict) -> BaseAdapter:
        adapter_type = adapter_config["adapter"]
        adapter_params = adapter_config.copy()
        del adapter_params["adapter"]
        adapter_module = importlib.import_module(
            f"cache_pyramid.adapters.{adapter_type}_adapter"
        )
        adapter_class = getattr(
            adapter_module, self.__get_class_name(f"{adapter_type}_adapter")
        )
        return adapter_class(**adapter_params)

    def __get_class_name(self, module_name: str) -> str:
        return string.capwords(module_name.replace("_", " ")).replace(" ", "")

    def getAdapters(self) -> List[BaseAdapter]:
        return self._adapters

    def setAdapters(self, adapters: List[BaseAdapter]) -> None:
        self._adapters = adapters

    def setAdapter(self, adapter: BaseAdapter, position: int) -> None:
        if position > len(self._adapters):
            raise IndexError
        if position == len(self._adapters):
            self._adapters.append(adapter)
        self._adapters[position] = adapter

    def get(self, key: str) -> Optional[Any]:
        for i, adapter in enumerate(self._adapters):
            result = adapter.get(key)
            if result is not None:
                # populate higher-level layers
                for higher_adapter in self._adapters[:i]:
                    higher_adapter.set(key, result)
                return result
        return None

    def mget(self, keys: List[str]) -> Dict[str, Optional[Any]]:
        result = {}
        remaining_keys = keys[:]
        highest_level_adapter_used = len(self._adapters)

        for i, adapter in enumerate(self._adapters):
            if not remaining_keys:
                highest_level_adapter_used = i
                break

            partial_result = adapter.mget(remaining_keys)
            for key, value in partial_result.items():
                if value is not None:
                    result[key] = value
                    remaining_keys.remove(key)
        if result:
            for higher_adapter in self._adapters[:highest_level_adapter_used]:
                higher_adapter.mset(result)

        return result

    def set(self, key: str, value: Any) -> None:
        for adapter in self._adapters:
            adapter.set(key, value)

    def mset(self, items: Dict[str, Any]) -> None:
        for adapter in self._adapters:
            adapter.mset(items)

    def delete(self, key: str) -> None:
        for adapter in self._adapters:
            adapter.delete(key)

    def exists(self, key: str) -> bool:
        for adapter in self._adapters:
            if adapter.exists(key):
                return True
        return False

    def flush(self) -> None:
        for adapter in self._adapters:
            adapter.flush()
