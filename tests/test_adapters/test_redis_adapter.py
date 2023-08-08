from typing import Iterator
from cache_tower.adapters.redis_adapter import RedisAdapter
import pytest
import redis


@pytest.fixture
def redis_client() -> Iterator[redis.Redis]:
    redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    redis_client.flushdb()
    yield redis_client
    redis_client.close()


def test_get(redis_client: redis.Redis):
    adapter = RedisAdapter(
        {"host": "localhost", "port": 6379, "db": 0, "decode_responses": True},
        "namespace:",
        60,
    )

    redis_client.set("namespace:key", "value")

    assert redis_client.get("namespace:key") == "value"
    assert adapter.get("key") == "value"


def test_set(redis_client: redis.Redis):
    adapter = RedisAdapter(
        {"host": "localhost", "port": 6379, "db": 0, "decode_responses": True},
        "namespace:",
        60,
    )

    assert redis_client.exists("namespace:key") == 0

    adapter.set("key", "value")

    assert redis_client.exists("namespace:key") == 1
    assert redis_client.get("namespace:key") == "value"
    assert redis_client.ttl("namespace:key") > 59
    assert redis_client.ttl("namespace:key") <= 60
    assert adapter.exists("key")
    assert adapter.get("key") == "value"


def test_delete(redis_client: redis.Redis):
    adapter = RedisAdapter(
        {"host": "localhost", "port": 6379, "db": 0, "decode_responses": True},
        "namespace:",
        60,
    )

    redis_client.set("namespace:key", "value")
    assert redis_client.exists("namespace:key") == 1

    adapter.delete("key")
    assert redis_client.exists("namespace:key") == 0


def test_mget(redis_client: redis.Redis):
    adapter = RedisAdapter(
        {"host": "localhost", "port": 6379, "db": 0, "decode_responses": True},
        "namespace:",
        60,
    )

    redis_client.set("namespace:key1", "value1")
    redis_client.set("namespace:key2", "value2")
    redis_client.set("namespace:key3", "value3")
    assert redis_client.exists("namespace:key1") == 1
    assert redis_client.exists("namespace:key2") == 1
    assert redis_client.exists("namespace:key3") == 1
    assert redis_client.get("namespace:key1") == "value1"
    assert redis_client.get("namespace:key2") == "value2"
    assert redis_client.get("namespace:key3") == "value3"

    result = adapter.mget(["key1", "key4", "key2"])

    assert "key1" in result
    assert result["key1"] == "value1"
    assert "key2" in result
    assert result["key2"] == "value2"
    assert "key4" in result
    assert result["key4"] is None
    assert len(result) == 3


def test_mset(redis_client: redis.Redis):
    adapter = RedisAdapter(
        {"host": "localhost", "port": 6379, "db": 0, "decode_responses": True},
        "namespace:",
        60,
    )

    assert redis_client.exists("namespace:key1") == 0
    assert redis_client.exists("namespace:key2") == 0

    adapter.mset({"key1": "value1", "key2": "value2"})

    assert redis_client.exists("namespace:key1") == 1
    assert redis_client.exists("namespace:key2") == 1
    assert redis_client.get("namespace:key1") == "value1"
    assert redis_client.get("namespace:key2") == "value2"
    assert redis_client.ttl("namespace:key1") > 59
    assert redis_client.ttl("namespace:key1") <= 60
    assert redis_client.ttl("namespace:key2") > 59
    assert redis_client.ttl("namespace:key2") <= 60


def test_flush():
    adapter = RedisAdapter(
        {"host": "localhost", "port": 6379, "db": 0, "decode_responses": True},
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
