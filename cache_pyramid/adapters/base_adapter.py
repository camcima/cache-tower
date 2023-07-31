from typing import Any, Dict, List, Optional


class BaseAdapter:
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
