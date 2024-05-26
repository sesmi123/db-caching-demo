import json
from models import Item


class WriteThroughCache:
    def __init__(self, db, cache_instance, logger):
        self.db = db
        self.cache = cache_instance
        self.logger = logger

    def add_data(self, data):
        item = Item(name=data['name'], description=data['description'])
        self.db.session.add(item)
        self.db.session.commit()
        # Update cache
        self.cache.setex(data['name'], 3600, json.dumps(data))
        self.logger.info("write-around ==> add_item: Cache updated!")
        return json.loads(item)
