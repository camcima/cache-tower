from cache_tower.adapters.memory_adapter import MemoryAdapter
from cache_tower.adapters.redis_adapter import RedisAdapter
from cache_tower.cache_tower import CacheTower
import pytest


def test_initialize_class():
    empty_param_cache = CacheTower()
    assert isinstance(empty_param_cache, CacheTower)

    zero_layer_cache = CacheTower([])
    assert isinstance(zero_layer_cache, CacheTower)

    one_layer_cache = CacheTower([{"adapter": "memory"}])
    assert isinstance(one_layer_cache, CacheTower)
    assert len(one_layer_cache.get_layers()) == 1

    two_layer_cache = CacheTower([{"adapter": "memory"}, {"adapter": "memory"}])
    assert isinstance(two_layer_cache, CacheTower)
    assert len(two_layer_cache.get_layers()) == 2

    three_layer_cache = CacheTower(
        [{"adapter": "memory"}, {"adapter": "memory"}, {"adapter": "memory"}]
    )
    assert isinstance(three_layer_cache, CacheTower)
    assert len(three_layer_cache.get_layers()) == 3

    redis_cache = CacheTower(
        [
            {"adapter": "memory", "namespace": "namespace-", "ttl": 60, "params": {}},
            {
                "adapter": "redis",
                "namespace": "redis-",
                "ttl": 3600,
                "params": {
                    "host": "localhost",
                    "port": 6379,
                    "db": 0,
                    "decode_responses": True,
                },
            },
        ]
    )
    redis_cache_adapters = redis_cache.get_layers()
    assert isinstance(three_layer_cache, CacheTower)
    assert len(redis_cache_adapters) == 2
    assert isinstance(redis_cache_adapters[0], MemoryAdapter)
    assert isinstance(redis_cache_adapters[1], RedisAdapter)


def test_add_layer():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()

    cache = CacheTower({})
    cache.add_layer(layer0)

    result = cache.get_layers()
    assert result[0] is layer0
    assert len(result) == 1

    cache.add_layer(layer1)

    result = cache.get_layers()
    assert result[0] is layer0
    assert result[1] is layer1
    assert len(result) == 2


def test_get_layers():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()

    cache = CacheTower({})
    cache.set_layer(layer0, 0)
    cache.set_layer(layer1, 1)

    result = cache.get_layers()

    assert result[0] is layer0
    assert result[1] is layer1
    assert len(result) == 2


def test_set_layers_from_empty():
    cache = CacheTower([])
    assert len(cache.get_layers()) == 0

    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()

    cache.set_layers([layer0, layer1])
    result = cache.get_layers()

    assert result[0] is layer0
    assert result[1] is layer1
    assert len(result) == 2


def test_set_layer_from_empty():
    cache = CacheTower([])

    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()

    with pytest.raises(IndexError):
        cache.set_layer(layer1, 1)

    cache.set_layer(layer0, 0)
    adapters = cache.get_layers()
    assert adapters[0] is layer0
    assert len(adapters) == 1

    cache.set_layer(layer1, 1)
    adapters = cache.get_layers()
    assert adapters[0] is layer0
    assert adapters[1] is layer1
    assert len(adapters) == 2


def test_set_layer():
    layer0 = MemoryAdapter()
    layer1 = MemoryAdapter()

    cache = CacheTower([])
    cache.set_layers([layer0, layer1])
    adapters = cache.get_layers()
    assert adapters[0] is layer0
    assert adapters[1] is layer1
    assert len(adapters) == 2

    new_layer0 = MemoryAdapter()
    cache.set_layer(new_layer0, 0)
    adapters = cache.get_layers()
    assert adapters[0] is not layer0
    assert adapters[0] is new_layer0
    assert adapters[1] is layer1
    assert len(adapters) == 2

    new_layer1 = MemoryAdapter()
    cache.set_layer(new_layer1, 1)
    adapters = cache.get_layers()
    assert adapters[0] is not layer0
    assert adapters[0] is new_layer0
    assert adapters[1] is not layer1
    assert adapters[1] is new_layer1
    assert len(adapters) == 2
