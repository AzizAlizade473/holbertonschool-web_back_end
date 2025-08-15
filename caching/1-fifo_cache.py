#!/usr/bin/python3
"""
1-fifo_cache module

So this code is apllying FIFO caching to the code and that is it
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFO class """

    def __init__(self):
        super().__init__()

    def put(self, key, item):
        """
        the put is for adding item
        """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.cache_data[key] = item
            return
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            first_key = next(iter(self.cache_data))
            print(f"DISCARD: {first_key}")
            del self.cache_data[first_key]
        self.cache_data[key] = item

    def get(self, key):
        """
        and this get is for illustrating needed element
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
