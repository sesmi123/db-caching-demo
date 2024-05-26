import json
from models import Item


class ReadThroughCache:
    def __init__(self, redis_instance, logger):
        self.redis = redis_instance
        self.logger = logger

    def get_data(self, key):
        data = self.redis.get(key)

        if data is None:
            self.logger.info("read-through ==> get_data: Cache miss!")
            data = Item.query.filter_by(name=key).first()
            if data:
                data = {'name': data.name, 'description': data.description}
                self.redis.setex(key, 3600, json.dumps(data))
                self.logger.info("read-through ==> get_data: Cache updated!")
            return data

        self.logger.info("read-through ==> get_data: Cache hit!")
        return json.loads(data)