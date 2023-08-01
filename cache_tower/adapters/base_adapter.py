from typing import Any, Dict, List, Optional


class BaseAdapter:
    def __init__(self, params: dict, namespace: str = "", ttl: int = 0) -> None:
        self._params: dict = params
        self._namespace: str = namespace
        self._ttl: int = ttl

    def _create_key(self, key: str) -> str:
        return self._namespace + key

    def _create_keys(self, keys: List[str]) -> List[str]:
        return [self._namespace + key for key in keys]

    def _create_items(self, items: Dict[str, Any]) -> Dict[str, Any]:
        return {self._create_key(key): value for key, value in items.items()}

    def get(self, key: str) -> Optional[Any]:
        raise NotImplementedError

    def mget(self, keys: List[str]) -> Dict[str, Optional[Any]]:
        raise NotImplementedError

    def set(self, key: str, value: Any) -> None:
        raise NotImplementedError

    def mset(self, items: Dict[str, Any]) -> None:
        raise NotImplementedError

    def delete(self, key: str) -> None:
        raise NotImplementedError

    def exists(self, key: str) -> bool:
        raise NotImplementedError

    def flush(self) -> None:
        raise NotImplementedError
