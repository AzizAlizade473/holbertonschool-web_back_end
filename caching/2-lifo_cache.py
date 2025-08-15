#!/usr/bin/python3
"""2-lifo_cache module."""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """LIFO caching system."""

    def __init__(self):
        super().__init__()
        self.keys_order = []

    def put(self, key, item):
        """Add an item in the cache."""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.keys_order.remove(key)
            self.keys_order.append(key)
            return

        self.cache_data[key] = item
        self.keys_order.append(key)

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            last_key = self.keys_order.pop(-2)
            del self.cache_data[last_key]
            print(f"DISCARD: {last_key}")

    def get(self, key):
        """Retrieve an item by key."""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
