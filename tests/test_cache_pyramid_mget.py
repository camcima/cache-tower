from cache_pyramid.adapters.memory_adapter import MemoryAdapter
from cache_pyramid.cache_pyramid import CachePyramid


def test_mget_one_layer():
    layer0 = MemoryAdapter()
    cache = CachePyramid([layer0])

    layer0.set("key1", "value1")
    layer0.set("key2", "value2")
    layer0.set("key3", "value3")

    result = cache.mget(["key1", "key2"])
    assert result["key1"] == "value1"
    assert result["key2"] == "value2"
    assert len(result) == 2


def test_mget_two_layers():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()
    cache = CachePyramid([layer0, layer1])

    # Testing layer 0
    layer0.set("key1", "value1")
    layer0.set("key2", "value2")
    layer0.set("key3", "value3")

    result = cache.mget(["key1", "key2"])
    assert result["key1"] == "value1"
    assert result["key2"] == "value2"
    assert len(result) == 2
    assert layer1.get("key1") is None
    assert layer1.get("key2") is None
    assert layer1.get("key3") is None

    # Testing layer 1
    layer0.flush()
    layer1.set("key1", "value1")
    layer1.set("key2", "value2")
    layer1.set("key3", "value3")

    result = cache.mget(["key1", "key2"])
    assert result["key1"] == "value1"
    assert result["key2"] == "value2"
    assert len(result) == 2
    assert len(result) == 2
    assert layer0.get("key1") == "value1"
    assert layer0.get("key2") == "value2"
    assert layer0.get("key3") is None


def test_mget_three_layers():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()
    layer2 = MemoryAdapter()
    cache = CachePyramid([layer0, layer1, layer2])

    # Testing layer 0
    layer0.set("key1", "value1")
    layer0.set("key2", "value2")
    layer0.set("key3", "value3")

    result = cache.mget(["key1", "key2"])
    assert result["key1"] == "value1"
    assert result["key2"] == "value2"
    assert len(result) == 2
    assert layer1.get("key1") is None
    assert layer1.get("key2") is None
    assert layer1.get("key3") is None
    assert layer2.get("key1") is None
    assert layer2.get("key2") is None
    assert layer2.get("key3") is None

    # Testing layer 1
    layer0.flush()
    layer1.set("key1", "value1")
    layer1.set("key2", "value2")
    layer1.set("key3", "value3")

    result = cache.mget(["key1", "key2"])
    assert result["key1"] == "value1"
    assert result["key2"] == "value2"
    assert len(result) == 2
    assert layer0.get("key1") == "value1"
    assert layer0.get("key2") == "value2"
    assert layer0.get("key3") is None
    assert layer2.get("key1") is None
    assert layer2.get("key2") is None
    assert layer2.get("key3") is None

    # Testing layer 2
    layer0.flush()
    layer1.flush()
    layer2.set("key1", "value1")
    layer2.set("key2", "value2")
    layer2.set("key3", "value3")

    result = cache.mget(["key1", "key2"])
    assert result["key1"] == "value1"
    assert result["key2"] == "value2"
    assert len(result) == 2
    assert layer0.get("key1") == "value1"
    assert layer0.get("key2") == "value2"
    assert layer0.get("key3") is None
    assert layer1.get("key1") == "value1"
    assert layer1.get("key2") == "value2"
    assert layer1.get("key3") is None
