from typing import Iterator
from cache_tower.adapters.memcached_adapter import MemcachedAdapter
from pymemcache.client.base import Client
import pytest


@pytest.fixture
def memcached_client() -> Iterator[Client]:
    memcached_client = Client(("localhost", 11211))
    memcached_client.flush_all()
    yield memcached_client
    memcached_client.close()


def test_invalid_client():
    with pytest.raises(RuntimeError):
        MemcachedAdapter(
            {"client_type": "invalid_client", "server": ("localhost", 11211)},
            "namespace:",
            60,
        )


def test_get(memcached_client: Client):
    adapter = MemcachedAdapter(
        {"client_type": "client", "server": ("localhost", 11211)}, "namespace:", 60
    )

    memcached_client.set("namespace:key", "value")

    assert memcached_client.get("namespace:key") == b"value"
    assert adapter.get("key") == "value"


def test_set(memcached_client: Client):
    adapter = MemcachedAdapter(
        {"client_type": "client", "server": ("localhost", 11211)}, "namespace:", 60
    )

    assert bool(memcached_client.get("namespace:key")) is False

    adapter.set("key", "value")

    memcached_client.touch("namespace:key")  # Avoids flaky tests
    assert bool(memcached_client.get("namespace:key")) is True
    assert memcached_client.get("namespace:key") == b"value"
    assert adapter.exists("key")
    assert adapter.get("key") == "value"


def test_delete(memcached_client: Client):
    adapter = MemcachedAdapter(
        {"client_type": "client", "server": ("localhost", 11211)}, "namespace:", 60
    )

    memcached_client.set("namespace:key", "value")
    assert bool(memcached_client.get("namespace:key")) is True

    adapter.delete("key")

    adapter.get("key")
    assert bool(memcached_client.get("namespace:key")) is False


def test_mget(memcached_client: Client):
    adapter = MemcachedAdapter(
        {"client_type": "client", "server": ("localhost", 11211)}, "namespace:", 60
    )

    memcached_client.set("namespace:key1", "value1")
    memcached_client.set("namespace:key2", "value2")
    memcached_client.set("namespace:key3", "value3")
    assert bool(memcached_client.get("namespace:key1")) is True
    assert bool(memcached_client.get("namespace:key2")) is True
    assert bool(memcached_client.get("namespace:key3")) is True
    assert memcached_client.get("namespace:key1") == b"value1"
    assert memcached_client.get("namespace:key2") == b"value2"
    assert memcached_client.get("namespace:key3") == b"value3"

    result = adapter.mget(["key1", "key4", "key2"])

    assert "key1" in result
    assert result["key1"] == "value1"
    assert "key4" in result
    assert result["key4"] is None
    assert "key2" in result
    assert result["key2"] == "value2"
    assert len(result) == 3


def test_mset(memcached_client: Client):
    adapter = MemcachedAdapter(
        {"client_type": "client", "server": ("localhost", 11211)}, "namespace:", 60
    )

    assert bool(memcached_client.get("namespace:key1")) is False
    assert bool(memcached_client.get("namespace:key2")) is False

    adapter.mset({"key1": "value1", "key2": "value2"})

    memcached_client.touch("namespace:ke1")  # avoiding flaky tests
    assert bool(memcached_client.get("namespace:key1")) is True
    assert bool(memcached_client.get("namespace:key2")) is True
    assert memcached_client.get("namespace:key1") == b"value1"
    assert memcached_client.get("namespace:key2") == b"value2"


def test_flush():
    adapter = MemcachedAdapter(
        {"client_type": "client", "server": ("localhost", 11211)}, "namespace:", 60
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
