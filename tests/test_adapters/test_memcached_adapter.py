from typing import Iterator
from cache_tower.adapters.memcached_adapter import MemcachedAdapter
from pymemcache.client.base import Client
from pymemcache import serde
import pytest


@pytest.fixture
def memcached_client() -> Iterator[Client]:
    memcached_client = Client(("localhost", 11211))
    memcached_client.flush_all()
    yield memcached_client
    memcached_client.close()


def test_get(memcached_client: Client):
    adapter = MemcachedAdapter(
        {"client_type": "client", "server": ("localhost", 11211)},
        "namespace:",
        60,
    )

    memcached_client.set("namespace:key", "value")

    assert memcached_client.get("namespace:key") == b"value"
    assert adapter.get("key") == b"value"


def test_set(memcached_client: Client):
    adapter = MemcachedAdapter(
        {"client_type": "client", "server": ("localhost", 11211)},
        "namespace:",
        60,
    )

    assert bool(memcached_client.get("namespace:key")) == False

    adapter.set("key", "value")

    assert bool(memcached_client.get(b"namespace:key")) == True
    assert memcached_client.get(b"namespace:key") == b"value"
    assert adapter.exists("key")
    assert adapter.get("key") == b"value"


def test_delete(memcached_client: Client):
    adapter = MemcachedAdapter(
        {"client_type": "client", "server": ("localhost", 11211)},
        "namespace:",
        60,
    )

    memcached_client.set("namespace:key", "value")
    assert bool(bool(memcached_client.get("namespace:key"))) == True

    adapter.delete("key")
    assert bool(bool(memcached_client.get("namespace:key"))) == False


def test_mget(memcached_client: Client):
    adapter = MemcachedAdapter(
        {"client_type": "client", "server": ("localhost", 11211)},
        "namespace:",
        60,
    )

    memcached_client.set("namespace:key1", "value1")
    memcached_client.set("namespace:key2", "value2")
    memcached_client.set("namespace:key3", "value3")
    assert bool(memcached_client.get("namespace:key1")) == True
    assert bool(memcached_client.get("namespace:key2")) == True
    assert bool(memcached_client.get("namespace:key3")) == True
    assert memcached_client.get("namespace:key1") == "value1"
    assert memcached_client.get("namespace:key2") == "value2"
    assert memcached_client.get("namespace:key3") == "value3"

    result = adapter.mget(["key1", "key2"])

    assert "key1" in result
    assert result["key1"] == "value1"
    assert "key2" in result
    assert result["key2"] == "value2"
    assert len(result) == 2


def test_mset(memcached_client: Client):
    adapter = MemcachedAdapter(
        {"client_type": "client", "server": ("localhost", 11211)},
        "namespace:",
        60,
    )

    assert bool(memcached_client.get("namespace:key1")) == False
    assert bool(memcached_client.get("namespace:key2")) == False

    adapter.mset({"key1": "value1", "key2": "value2"})

    assert bool(memcached_client.get("namespace:key1")) == True
    assert bool(memcached_client.get("namespace:key2")) == True
    assert memcached_client.get("namespace:key1") == "value1"
    assert memcached_client.get("namespace:key2") == "value2"
    assert memcached_client.ttl("namespace:key1") > 59
    assert memcached_client.ttl("namespace:key1") <= 60
    assert memcached_client.ttl("namespace:key2") > 59
    assert memcached_client.ttl("namespace:key2") <= 60


def test_flush():
    adapter = MemcachedAdapter(
        {"client_type": "client", "server": ("localhost", 11211)},
        "namespace:",
        60,
    )

    adapter.set("key1", "value1")
    adapter.mset({"key2": "value2", "key3": "value3"})
    assert adapter.get("key1") == "value1"
    assert adapter.get("key2") == "value2"
    assert adapter.get("key3") == "value3"

    adapter.flush()
    assert not adapter.exists("key1")
    assert not adapter.exists("key2")
    assert not adapter.exists("key3")
    assert adapter.get("key1") is None
    assert adapter.get("key2") is None
    assert adapter.get("key3") is None
