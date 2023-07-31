from cache_pyramid.adapters.memory_adapter import MemoryAdapter
from cache_pyramid.cache_pyramid import CachePyramid


def test_delete_one_layer():
    layer0 = MemoryAdapter()
    cache = CachePyramid([layer0])

    layer0.set("key", "value")
    assert cache.get("key") == "value"

    cache.delete("key")
    assert not cache.exists("key")
    assert cache.get("key") == None
    assert not layer0.exists("key")


def test_delete_two_layers():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()
    cache = CachePyramid([layer0, layer1])

    layer0.set("key", "value")
    layer1.set("key", "value")
    assert cache.get("key") == "value"

    cache.delete("key")
    assert not cache.exists("key")
    assert cache.get("key") == None
    assert not layer0.exists("key")
    assert not layer1.exists("key")


def test_delete_three_layers():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()
    layer2 = MemoryAdapter()
    cache = CachePyramid([layer0, layer1, layer2])

    layer0.set("key", "value")
    layer1.set("key", "value")
    layer2.set("key", "value")
    assert cache.get("key") == "value"

    cache.delete("key")
    assert not cache.exists("key")
    assert cache.get("key") == None
    assert not layer0.exists("key")
    assert not layer1.exists("key")
    assert not layer2.exists("key")