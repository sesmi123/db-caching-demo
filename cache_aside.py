import json


class CacheAside:
    def __init__(self, cache_instance, logger):
        self.cache = cache_instance
        self.logger = logger

    def get_data(self, name):
        # Check cache first
        cached_item = self.cache.get(name)
        if cached_item:
            self.logger.info("cache-aside ==> get_item: Cache hit!")
            return json.loads(cached_item)
        
        return None
    
    def set_data(self, key, data):
        self.cache.setex(key, 3600, data)
