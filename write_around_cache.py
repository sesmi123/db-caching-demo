import json
from models import Item


class WriteAroundCache:
    def __init__(self, db, cache_instance, logger):
        self.db = db
        self.cache = cache_instance
        self.logger = logger

    def add_data(self, data):
        # Write-Around: Write directly to the database and invalidate the cache entry
        # This particular strategy is going to be most performant in instances where data is only written once and not updated.
        # The data is read very infrequently or not at all.
        item = Item(name=data['name'], description=data['description'])
        self.db.session.add(item)
        self.db.session.commit()
        # Optional: Invalidate cache
        self.cache.delete(data['name'])
        self.logger.info("write-around ==> add_item: Cache invalidated!")
        return json.loads(item)
