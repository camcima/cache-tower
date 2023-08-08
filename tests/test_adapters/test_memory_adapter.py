from time import sleep
from cache_tower.adapters.memory_adapter import MemoryAdapter


def test_set_and_get():
    adapter = MemoryAdapter({}, "namespace:")

    adapter.set("key", "value")

    assert adapter.get("key") == "value"


def test_set_maxsize():
    adapter = MemoryAdapter({"maxsize": 2}, "namespace:")

    adapter.set("key1", "value1")
    assert adapter.get("key1") == "value1"

    adapter.set("key2", "value2")
    assert adapter.get("key2") == "value2"
    assert adapter.get("key1") == "value1"

    adapter.set("key3", "value3")
    assert adapter.get("key1") is None
    assert adapter.get("key3") == "value3"
    assert adapter.get("key2") == "value2"

    adapter.set("key4", "value4")
    assert adapter.get("key1") is None
    assert adapter.get("key2") is None
    assert adapter.get("key3") == "value3"
    assert adapter.get("key4") == "value4"


def test_set_maxsize_lru():
    adapter = MemoryAdapter({"maxsize": 2, "lru": True}, "namespace:")

    adapter.set("key1", "value1")
    assert adapter.get("key1") == "value1"

    adapter.set("key2", "value2")
    assert adapter.get("key2") == "value2"
    assert adapter.get("key1") == "value1"

    adapter.set("key3", "value3")
    assert adapter.get("key3") == "value3"
    assert adapter.get("key1") == "value1"
    assert adapter.get("key2") is None

    adapter.set("key4", "value4")
    assert adapter.get("key1") == "value1"
    assert adapter.get("key2") is None
    assert adapter.get("key3") is None
    assert adapter.get("key4") == "value4"


def test_get_not_exists():
    adapter = MemoryAdapter({}, "namespace:")

    assert adapter.get("foo") is None


def test_get_expired_key():
    adapter = MemoryAdapter({}, "namespace:", 1)

    adapter.set("key", "value")
    assert adapter.get("key") == "value"
    sleep(1)
    assert adapter.get("key") is None


def test_exists():
    adapter = MemoryAdapter({}, "namespace:")

    assert not adapter.exists("key")

    adapter.set("key", "value")

    assert adapter.exists("key")


def test_delete():
    adapter = MemoryAdapter({}, "namespace:")

    adapter.set("key", "value")

    adapter.delete("key")

    assert not adapter.exists("key")
    assert adapter.get("key") is None


def test_mget():
    adapter = MemoryAdapter({}, "namespace:")

    adapter.set("key1", "value1")
    adapter.set("key2", "value2")
    adapter.set("key3", "value3")

    values = adapter.mget(["key1", "key4", "key2"])

    assert "key1" in values
    assert "key2" in values
    assert "key4" in values
    assert values["key1"] == "value1"
    assert values["key2"] == "value2"
    assert values["key4"] is None
    assert len(values) == 3


def test_mset():
    adapter = MemoryAdapter({}, "namespace:")

    adapter.mset({"key1": "value1", "key2": "value2"})

    assert adapter.exists("key1")
    assert adapter.exists("key2")
    assert adapter.get("key1") == "value1"
    assert adapter.get("key2") == "value2"


def test_flush():
    adapter = MemoryAdapter({}, "namespace:")

    adapter.set("key1", "value1")
    adapter.mset({"key2": "value2", "key3": "value3"})
    assert adapter.get("key1") == "value1"
    assert adapter.get("key2") == "value2"
    assert adapter.get("key3") == "value3"

    adapter.flush()
    assert not adapter.exists("key1")
    assert not adapter.exists("key2")
    assert not adapter.exists("key3")
    assert adapter.get("key1") is None
    assert adapter.get("key2") is None
    assert adapter.get("key3") is None
