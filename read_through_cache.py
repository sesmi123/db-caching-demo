import json
from models import Item


class ReadThroughCache:
    def __init__(self, cache_instance, logger):
        self.cache = cache_instance
        self.logger = logger

    def get_data(self, key):
        data = self.cache.get(key)

        if data:
            self.logger.info("read-through ==> get_data: Cache hit!")
            return json.loads(data)
        
        self.logger.info("read-through ==> get_data: Cache miss!")
        data = Item.query.filter_by(name=key).first()

        if data:
            data = {'name': data.name, 'description': data.description}
            self.cache.setex(key, 3600, json.dumps(data))
            self.logger.info("read-through ==> get_data: Cache updated!")
        
        return data
