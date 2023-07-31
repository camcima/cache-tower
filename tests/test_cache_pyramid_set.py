from cache_pyramid.adapters.memory_adapter import MemoryAdapter
from cache_pyramid.cache_pyramid import CachePyramid


def test_set_one_layer():
    layer0 = MemoryAdapter()
    cache = CachePyramid([layer0])

    cache.set("key", "value")

    assert layer0.get("key") == "value"

    cache.set("key", "foo")

    assert layer0.get("key") == "foo"


def test_set_two_layers():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()
    cache = CachePyramid([layer0, layer1])

    cache.set("key", "value")

    assert layer0.get("key") == "value"
    assert layer1.get("key") == "value"

    cache.set("key", "foo")

    assert layer0.get("key") == "foo"
    assert layer1.get("key") == "foo"


def test_set_three_layers():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()
    layer2 = MemoryAdapter()
    cache = CachePyramid([layer0, layer1, layer2])

    cache.set("key", "value")

    assert layer0.get("key") == "value"
    assert layer1.get("key") == "value"
    assert layer2.get("key") == "value"

    cache.set("key", "foo")

    assert layer0.get("key") == "foo"
    assert layer1.get("key") == "foo"
    assert layer2.get("key") == "foo"
