import json
from models import Item


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

        # Cache miss, query database
        self.logger.info("cache-aside ==> get_item: Cache miss!")
        item = Item.query.filter_by(name=name).first()
        
        # update cache
        if item:
            # cahce for 1 hour
            self.cache.setex(name, 3600, json.dumps({'name': item.name, 'description': item.description}))
            self.logger.info("cache-aside ==> get_item: Cache updated!")
            return {'name': item.name, 'description': item.description}
        
        return None
