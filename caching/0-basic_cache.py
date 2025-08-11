#!/usr/bin/python3
""" BasicCache module
Defines a BasicCache class that inherits from BaseCaching
and is a caching system without limit.
"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """ BasicCache is a caching system without limit """

    def put(self, key, item):
        """
        Add an item in the cache.
        If key or item is None, do nothing.
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """
        Get an item by key.
        Return None if key is None or key does not exist.
        """
        if key is None:
            return None
        return self.cache_data.get(key)
