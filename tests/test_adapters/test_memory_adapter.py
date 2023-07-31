from cache_pyramid.adapters.memory_adapter import MemoryAdapter


def test_set_and_get():
    adapter = MemoryAdapter()

    adapter.set("key", "value")

    assert adapter.get("key") == "value"


def test_get_not_exists():
    adapter = MemoryAdapter()

    assert adapter.get("foo") == None


def test_exists():
    adapter = MemoryAdapter()

    assert not adapter.exists("key")

    adapter.set("key", "value")

    assert adapter.exists("key")


def test_delete():
    adapter = MemoryAdapter()

    adapter.set("key", "value")

    adapter.delete("key")

    assert not adapter.exists("key")
    assert adapter.get("key") == None


def test_mget():
    adapter = MemoryAdapter()

    adapter.set("key1", "value1")
    adapter.set("key2", "value2")
    adapter.set("key3", "value3")

    values = adapter.mget(["key1", "key2"])

    assert "key1" in values
    assert "key2" in values
    assert values["key1"] == "value1"
    assert values["key2"] == "value2"
    assert len(values) == 2


def test_mset():
    adapter = MemoryAdapter()

    adapter.mset({"key1": "value1", "key2": "value2"})

    assert adapter.exists("key1")
    assert adapter.exists("key2")
    assert adapter.get("key1") == "value1"
    assert adapter.get("key2") == "value2"


def test_flush():
    adapter = MemoryAdapter()

    adapter.set("key1", "value1")
    adapter.mset({"key2": "value2", "key3": "value3"})
    assert adapter.get("key1") == "value1"
    assert adapter.get("key2") == "value2"
    assert adapter.get("key3") == "value3"

    adapter.flush()
    assert not adapter.exists("key1")
    assert not adapter.exists("key2")
    assert not adapter.exists("key3")
    assert adapter.get("key1") == None
    assert adapter.get("key2") == None
    assert adapter.get("key3") == None
