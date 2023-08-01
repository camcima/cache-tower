from cache_tower.adapters.memory_adapter import MemoryAdapter
from cache_tower.cache_tower import CacheTower


def test_mset_one_layer():
    layer0 = MemoryAdapter()
    cache = CacheTower([])
    cache.setAdapters([layer0])

    cache.mset({"key1": "value1", "key2": "value2"})

    assert layer0.get("key1") == "value1"
    assert layer0.get("key2") == "value2"

    cache.mset({"key1": "foo1", "key2": "foo2"})

    assert layer0.get("key1") == "foo1"
    assert layer0.get("key2") == "foo2"


def test_mset_two_layers():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()
    cache = CacheTower([])
    cache.setAdapters([layer0, layer1])

    cache.mset({"key1": "value1", "key2": "value2"})

    assert layer0.get("key1") == "value1"
    assert layer0.get("key2") == "value2"
    assert layer1.get("key1") == "value1"
    assert layer1.get("key2") == "value2"

    cache.mset({"key1": "foo1", "key2": "foo2"})

    assert layer0.get("key1") == "foo1"
    assert layer0.get("key2") == "foo2"
    assert layer1.get("key1") == "foo1"
    assert layer1.get("key2") == "foo2"


def test_mset_three_layers():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()
    layer2 = MemoryAdapter()
    cache = CacheTower([])
    cache.setAdapters([layer0, layer1, layer2])

    cache.mset({"key1": "value1", "key2": "value2"})

    assert layer0.get("key1") == "value1"
    assert layer0.get("key2") == "value2"
    assert layer1.get("key1") == "value1"
    assert layer1.get("key2") == "value2"
    assert layer2.get("key1") == "value1"
    assert layer2.get("key2") == "value2"

    cache.mset({"key1": "foo1", "key2": "foo2"})

    assert layer0.get("key1") == "foo1"
    assert layer0.get("key2") == "foo2"
    assert layer1.get("key1") == "foo1"
    assert layer1.get("key2") == "foo2"
    assert layer2.get("key1") == "foo1"
    assert layer2.get("key2") == "foo2"
