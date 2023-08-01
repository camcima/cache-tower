from cache_pyramid.adapters.memory_adapter import MemoryAdapter
from cache_pyramid.cache_pyramid import CachePyramid
import pytest


def test_initialize_class():
    with pytest.raises(TypeError):
        CachePyramid() # Invalid initialization

    empty_cache = CachePyramid([])
    assert isinstance(empty_cache, CachePyramid)


def test_get_adapters():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()

    cache = CachePyramid([layer0, layer1])

    result = cache.getAdapters()

    assert result[0] is layer0
    assert result[1] is layer1
    assert len(result) == 2


def test_set_adapters_from_empty():
    cache = CachePyramid([])
    assert len(cache.getAdapters()) == 0

    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()

    cache.setAdapters([layer0, layer1])
    result = cache.getAdapters()

    assert result[0] is layer0
    assert result[1] is layer1
    assert len(result) == 2


def test_set_adapter_from_empty():
    cache = CachePyramid([])

    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()

    with pytest.raises(IndexError):
        cache.setAdapter(layer1, 1)

    cache.setAdapter(layer0, 0)
    adapters = cache.getAdapters()
    assert adapters[0] is layer0
    assert len(adapters) == 1

    cache.setAdapter(layer1, 1)
    adapters = cache.getAdapters()
    assert adapters[0] is layer0
    assert adapters[1] is layer1
    assert len(adapters) == 2


def test_set_adapter():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()

    cache = CachePyramid([layer0, layer1])
    adapters = cache.getAdapters()
    assert adapters[0] is layer0
    assert adapters[1] is layer1
    assert len(adapters) == 2

    new_layer0 = MemoryAdapter()
    cache.setAdapter(new_layer0, 0)
    adapters = cache.getAdapters()
    assert not adapters[0] is layer0
    assert adapters[0] is new_layer0
    assert adapters[1] is layer1
    assert len(adapters) == 2

    new_layer1 = MemoryAdapter()
    cache.setAdapter(new_layer1, 1)
    adapters = cache.getAdapters()
    assert not adapters[0] is layer0
    assert adapters[0] is new_layer0
    assert not adapters[1] is layer1
    assert adapters[1] is new_layer1
    assert len(adapters) == 2
