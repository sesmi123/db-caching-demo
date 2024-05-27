import json
from models import Item


class WriteThroughCache:
    def __init__(self, db, cache_instance, logger):
        self.db = db
        self.cache = cache_instance
        self.logger = logger

    def add_data(self, data):
        item = Item(name=data['name'], description=data['description'])
        try:
            # Write to database
            self.db.session.add(item)
            self.db.session.commit()
            # Update cache
            self.cache.setex(data['name'], 3600, json.dumps(data))
            self.logger.info("write-around ==> add_item: Cache updated!")
        except Exception as e:
            # Rollback database transaction if any error occurs
            self.db.session.rollback()
            # Delete the cache entry if it was created
            self.cache.delete(data['name'])
            self.logger.error("Error in add_data: ", e)
            raise
        return data
