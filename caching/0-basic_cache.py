
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    

    def put(self, key, item):
        
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        
        if key is None:
            return None
        return self.cache_data.get(key)
