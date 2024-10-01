"""
Module for managing Redis cache operations using the `redis-py` client.

This module provides functions and classes to interact with a Redis cache,
allowing you to store and retrieve data efficiently. It includes:
- `redis_cache` function: Initializes a Redis client and returns a `RedisCache` instance.
- `RedisCache` class: Provides `get` and `set` methods to interact with Redis.

Typical usage example:

    cache = redis_cache(host='localhost', port=6379)
    cache.set('some_key', {'data': 'value'})
    result = cache.get('some_key')

This module is designed to make cache operations in Redis simple and efficient.
"""

import json
import redis


def redis_cache(host="localhost", port=6379):
    """
    Initializes a Redis client and returns a RedisCache instance.

    Args:
        host (str): The Redis server hostname. Defaults to 'localhost'.
        port (int): The Redis server port. Defaults to 6379.

    Returns:
        RedisCache: An instance of the RedisCache class.
    """

    client = redis.StrictRedis(host=host, port=port, decode_responses=True)
    return RedisCache(client)


class RedisCache:
    """
    A cache handler class that interfaces with Redis for caching operations.

    Attributes:
        client (StrictRedis): Redis client used for interaction with Redis.
    """

    def __init__(self, client):
        """
        Initializes the RedisCache instance with a Redis client.

        Args:
            client (StrictRedis): The Redis client used for connection to the Redis server.
        """

        self.client = client

    def get(self, key):
        """
        Retrieves a value from Redis cache for a given key.

        Args:
            key (str): The key used to look up the cache.

        Returns:
            dict or None: The cached data as a Python dictionary if the key exists,
                          otherwise None.
        """

        cached_data = self.client.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None

    def set(self, key, value, expiration=3600):
        """
        Stores a value in Redis cache with an optional expiration time.

        Args:
            key (str): The key to store the cache under.
            value (dict): The value to cache (as a Python dictionary).
            expiration (int): The cache expiration time in seconds. Defaults to 3600 (1 hour).
        """

        self.client.set(key, json.dumps(value), ex=expiration)
