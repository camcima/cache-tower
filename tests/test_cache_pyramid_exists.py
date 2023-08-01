from cache_tower.adapters.memory_adapter import MemoryAdapter
from cache_tower.cache_tower import CacheTower


def test_exists_one_layer():
    layer0 = MemoryAdapter()
    cache = CacheTower([])
    cache.setAdapters([layer0])

    layer0.set("key", "value")
    assert cache.exists("key")


def test_exists_two_layers():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()
    cache = CacheTower([])
    cache.setAdapters([layer0, layer1])

    layer0.set("key", "value")
    assert cache.exists("key")

    layer0.delete("key")
    layer1.set("key", "value")
    assert cache.exists("key")

    layer0.set("key", "value")
    assert cache.exists("key")


def test_exists_three_layers():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()
    layer2 = MemoryAdapter()
    cache = CacheTower([])
    cache.setAdapters([layer0, layer1, layer2])

    # Layer 0
    layer0.set("key", "value")
    assert cache.exists("key")

    # Layer 1
    layer0.delete("key")
    layer1.set("key", "value")
    assert cache.exists("key")

    # Layer 2
    layer1.delete("key")
    layer2.set("key", "value")
    assert cache.exists("key")

    # Layers 0, 1
    layer2.delete("key")
    layer0.set("key", "value")
    layer1.set("key", "value")
    assert cache.exists("key")

    # Layers 0, 2
    layer1.delete("key")
    layer2.set("key", "value")
    assert cache.exists("key")

    # Layers 1, 2
    layer0.delete("key")
    layer1.set("key", "value")
    assert cache.exists("key")

    # Layers 0, 1, 2
    layer0.set("key", "value")
    assert cache.exists("key")
