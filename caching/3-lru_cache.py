#!/usr/bin/python3
"""3-lru_cache module."""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """LRU caching system."""

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
            lru_key = self.keys_order.pop(0)
            del self.cache_data[lru_key]
            print(f"DISCARD: {lru_key}")

    def get(self, key):
        """Show an item by key."""
        if key is None or key not in self.cache_data:
            return None
        self.keys_order.remove(key)
        self.keys_order.append(key)
        return self.cache_data[key]
