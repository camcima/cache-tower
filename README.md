![Build Status](https://github.com/camcima/cache-tower/actions/workflows/main.yml/badge.svg)
[![Coverage Status](https://codecov.io/gh/camcima/cache-tower/branch/main/graph/badge.svg?token=6EDFO4ECUG)](https://codecov.io/gh/camcima/cache-tower)

> **THIS PROJECT IS STILL UNDER DEVELOPMENT AND NOT READY TO BE USED**

# Cache Tower

Cache Tower is a simple and efficient multilevel caching library for Python.

## Installation

WIP

## Usage

### Initialization

Cache Tower provides two configuration methods: a dictionary-based configuration and a programmatic configuration. These methods allow you to define the number of caching layers, their respective adapters, namespaces, expiration times, and adapter-specific parameters.

#### Dictionary Method

With the dictionary method, you define your caching configuration in a dictionary that specifies the caching layers, the adapters for each level, namespaces, expiration times, and adapter-specific parameters.

**Example:**

```python
config = [
  {
    "adapter": "memory",
    "namespace": "session:",
    "ttl": 60,
    "params": {
      "maxsize": 1024,
      "lru": True
    }
  },
  {
    "adapter": "redis",
    "namespace": "session:",
    "ttl": 300,
    "params": {
      "host": "localhost",
      "port": 6379
      "db": 0,
      "decode_responses": True
    }
  }
]

cache = CacheTower(config)

cache.set("key", "value")
result = cache.get("key")
# result == "value"
```

This method is particularly useful when your caching configuration is retrieved from the application settings.

#### Programatic Method

The programmatic method involves creating an empty cache service and adding layers to it programmatically.

**Example:**

```python
cache = CacheTower()
cache.add_layer(
    MemoryAdapter(params={"maxsize": 1024, "lru": True}, namespace="session:", ttl=60)
)
cache.add_layer(
    RedisAdapter(
        params={"host": "localhost", "port": 6379, "db": 0, "decode_responses": True},
        namespace="session:",
        ttl=300,
    )
)

cache.set("key", "value")
result = cache.get("key")

# result == "value"
```

#### Layer Configuration Options

`adapter` (`str`): Specify the cache adapter for this layer. The current options are:
* `memory` In-memory cache (`MemoryAdapter` class)
* `redis` Redis server (`RedisAdapter` class)
* 
`namespace` (`str`): The namespace you want to use. Every key in the cache will be prefixed with chosen namespace. If you want to use specific separators for the namespaces (e.g. ":" for Redis), make sure the include it in the namespace string.

`ttl` (`int`): Time-to-live for every key in the cache (in seconds). Keys will be deleted from cache after the TTL has expired. Use `0` if you don't want the keys to expire.

### Layer Methods

#### `add_layer(adapter: BaseAdapter) -> None`

This method adds a new caching layer to the top of the stack. This layer will be the last one to be used in the event of a cache miss in the lower-level layers.

```python
cache = CacheTower()
cache.add_layer(MemoryAdapter())
```

#### `get_layers() -> List[BaseAdapter]`

This method returns a list of the current cache adapter stack. The adapters in the lower positions are used first.

```python
cache = CacheTower([{"adapter": "memory"}, {"adapter": "redis}])

layers = cache.get_layers()

# layers == [MemoryAdapter(), RedisAdapter()]
```

#### `set_layers(adapters: List[BaseAdapter]) -> None`

This method resets the cache adapter stack to the provided adapter list.

```python
cache = CacheTower([{"adapter": "memory"}, {"adapter": "redis}])

cache.set_layers([MemoryAdapter()])

layers = cache.getLayers()
# layers == [MemoryAdapter()]
```

#### `set_layer(adapter: BaseAdapter, position: int) -> None`

This method creates or replaces the cache adapter in a specific position in the stack. If the given position is occupied, the existing adapter will be replaced. If the position is at the end of the stack, the adapter will be appended. Invalid positions will result in an `IndexError`.

```python
# Replaces adapter
cache = CacheTower([{"adapter": "memory"}, {"adapter": "redis}])

cache.set_layer([MemoryAdapter()], 1)

layers = cache.get_layers()
# layers == [MemoryAdapter(), MemoryAdapter()]

# Adds adapter
cache = CacheTower([{"adapter": "memory"}, {"adapter": "redis}])

cache.set_layer([MemoryAdapter()], 2)

layers = cache.get_layers()
# layers == [MemoryAdapter(), RedisAdapter(), MemoryAdapter()]

```

### Cache Methods

#### `get(key: str) -> Optional[Any]`

This method retrieves the value of the given key from the cache. The first adapter in the stack is called, and if the key is found, the value is immediately returned. If the key is not found in the first adapter, the next adapter is called, and so on. If the key is found at a higher level, the key/value pair is added to the lower levels using the configured TTL for each adapter. This ensures that if the key is needed again, it can be served faster.

If the key is not found in any of the layers, this method will return `None`.

```python
cache = CacheTower([{"adapter": "memory"}, {"adapter": "redis}])

result = cache.get("key")

# result == "value"
```

#### `set(key: str, value: Any) -> None`

This method creates or replaces the key/value pair in all layers of the cache adapter stack using the configured TTL for each layer.

> Currently, keys are set synchronously in each layer. In future versions, keys will be set asynchronously.

```python
cache = CacheTower([{"adapter": "memory"}, {"adapter": "redis}])

cache.set("key", "value")
```

#### `mget(keys: List[str]) -> Dict[str, Optional[Any]]`

This method retrieves multiple keys from the cache. If a key is not found in any of the layers, it will still be returned in the resulting dictionary with a value of `None`. The rules for setting keys in lower levels in the event of cache misses are the same as in the `get()` method.

```python
cache = CacheTower([{"adapter": "memory"}, {"adapter": "redis}])

result = cache.get(["key1", "key2"])

# result == {"key1": "value1", "key2": "value2"}
```

#### `mset(items: Dict[str, Any]) -> None`

This method creates or replaces multiple key/value pairs in all layers of the cache adapter stack using the configured TTL for each layer.

```python
cache = CacheTower([{"adapter": "memory"}, {"adapter": "redis}])

cache.mset({"key1": "value1", "key2": "value2"})
```

#### `delete(key: str) -> None`

This method deletes a key from all layers.

```python
cache = CacheTower([{"adapter": "memory"}, {"adapter": "redis}])

cache.delete("key")
```

#### `exists(key: str) -> bool`

This method checks whether a given key exists in the cache. If the key is not found in the lower cache levels but is found in a higher level, the key will **not** be created in the lower levels.

```python
cache = CacheTower([{"adapter": "memory"}, {"adapter": "redis}])

result = cache.exists("key")

# result == True
```

#### `flush() -> None`

This method deletes the entire key set from all cache layers.

```python
cache = CacheTower([{"adapter": "memory"}, {"adapter": "redis}])

cache.flush()

# all cache layers are empty
```

### Cache Adapters

#### `MemoryAdapter`

The MemoryAdapter is an in-memory cache adapter implemented as an `OrderedDict`. It provides the fastest caching speed and should always be the lowest level layer in any stack.

**Configuration Parameters**

`maxsize` (`int`) - default `0`: This parameter sets the maximum number of keys allowed in the cache. If a key is added beyond this limit, the oldest key is removed by default. This behavior can be modified using the `lru` parameter. If this parameter is `0`, no size limit will be applied.

`lru` (`bool`) - default `False`: If this parameter is set to `True`, the eviction behavior of `maxsize` will change to delete the least recently used key, instead of the oldest one.

> The TTL implementation in this adapter is somewhat lax. The TTL will only be enforced when the key is accessed. This means that an expired key will remain in memory until it is accessed. Implementing an active purge of expired keys in the future would require a threaded implementation of a purging process.

#### `RedisAdapter`

The `RedisAdapter` is an adapter for the Redis Server. It uses the [redis](https://pypi.org/project/redis/) library. The configuration parameters are the same as in the original library and you can check them [here](https://redis-py.readthedocs.io/en/stable/connections.html).

## Multilevel Caching

Multilevel caching, also known as layered or hierarchical caching, is a strategy designed to enhance the performance and efficiency of web applications. It accomplishes this by storing data at various levels of the system. The aim is to increase data availability by reducing the time it takes to fetch it from the source. This strategy is grounded in the principle of locality, which asserts that data accessed once is likely to be accessed again in the near future.

Each level of cache typically has a different size. The fastest caches (like in-memory caches) are usually the smallest, while the slowest caches (like databases) are the largest.

These different levels of cache can be used together in a multilevel caching strategy. When data is requested, the application first checks the fastest cache. If the data is not there (a cache miss), it will check the next level, and so on, until the data is found or until the source of truth (like a database or an external API) is reached. When data is fetched from a slower level or the source, it is then placed in the faster caches. This ensures that future accesses to the same data will be faster.

It's important to note that effective cache management is complex. It requires careful consideration of factors such as the size, speed, volatility, consistency requirements, and cost of the different caches, as well as the specific access patterns and needs of the application.


