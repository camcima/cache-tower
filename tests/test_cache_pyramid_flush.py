from cache_pyramid.adapters.memory_adapter import MemoryAdapter
from cache_pyramid.cache_pyramid import CachePyramid


def test_flush_one_layer():
    layer0 = MemoryAdapter()
    cache = CachePyramid([layer0])

    layer0.set("key1", "value1")
    layer0.set("key2", "value2")

    cache.flush()
    assert not layer0.exists("key1")
    assert not layer0.exists("key2")


def test_flush_two_layers():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()
    cache = CachePyramid([layer0, layer1])

    layer0.set("key1", "value1")
    layer0.set("key2", "value2")
    layer1.set("key1", "value1")
    layer1.set("key2", "value2")

    cache.flush()
    assert not layer0.exists("key1")
    assert not layer0.exists("key2")
    assert not layer1.exists("key1")
    assert not layer1.exists("key2")


def test_flush_three_layers():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()
    layer2 = MemoryAdapter()
    cache = CachePyramid([layer0, layer1, layer2])

    layer0.set("key1", "value1")
    layer0.set("key2", "value2")
    layer1.set("key1", "value1")
    layer1.set("key2", "value2")
    layer2.set("key1", "value1")
    layer2.set("key2", "value2")

    cache.flush()
    assert not layer0.exists("key1")
    assert not layer0.exists("key2")
    assert not layer1.exists("key1")
    assert not layer1.exists("key2")
    assert not layer2.exists("key1")
    assert not layer2.exists("key2")
