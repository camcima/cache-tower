from cache_pyramid.adapters.memory_adapter import MemoryAdapter
from cache_pyramid.cache_pyramid import CachePyramid


def test_get_one_layer():
    layer0 = MemoryAdapter()
    cache = CachePyramid([])
    cache.setAdapters([layer0])

    layer0.set("key", "value")

    assert cache.get("key") == "value"


def test_get_two_layers():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()
    cache = CachePyramid([])
    cache.setAdapters([layer0, layer1])

    # Testing layer 0
    layer0.set("key", "value")
    assert cache.get("key") == "value"

    # Testing layer 1
    layer0.delete("key")
    assert layer0.get("key") is None
    layer1.set("key", "value")
    assert cache.get("key") == "value"
    assert layer0.get("key") == "value"


def test_get_three_layers():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()
    layer2 = MemoryAdapter()
    cache = CachePyramid([])
    cache.setAdapters([layer0, layer1, layer2])

    # Testing layer 0
    layer0.set("key", "value")
    assert cache.get("key") == "value"

    # Testing layer 1
    layer0.delete("key")
    assert layer0.get("key") is None
    layer1.set("key", "value")
    assert cache.get("key") == "value"
    assert layer0.get("key") == "value"
    assert layer1.get("key") == "value"
    assert layer2.get("key") is None

    # Testing layer 2
    layer0.delete("key")
    layer1.delete("key")
    assert layer0.get("key") is None
    layer2.set("key", "value")
    assert cache.get("key") == "value"
    assert layer0.get("key") == "value"
    assert layer1.get("key") == "value"
