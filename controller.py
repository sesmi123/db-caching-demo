
import json
from models import Item
from read_through_cache import ReadThroughCache



class APIController:

    def __init__(self, db, cache, logger):
        self.db = db
        self.cache = cache
        self.logger = logger
        self.rtc = ReadThroughCache(cache, logger)


    def read_through_get_item(self, name):
        item = self.rtc.get_data(name)
        if item:
            return item, 200
        return {'error': 'Item not found'}, 404

    def cache_aside_get_item(self, name):
        # Check cache first
        cached_item = self.cache.get(name)
        if cached_item:
            self.logger.info("cache-aside ==> get_item: Cache hit!")
            return json.loads(cached_item), 200

        # Cache miss, query database
        self.logger.info("cache-aside ==> get_item: Cache miss!")
        item = Item.query.filter_by(name=name).first()
        
        # update cache
        if item:
            # cahce for 1 hour
            self.cache.setex(name, 3600, json.dumps({'name': item.name, 'description': item.description}))
            self.logger.info("cache-aside ==> get_item: Cache updated!")
            return {'name': item.name, 'description': item.description}, 200
        return {'error': 'Item not found'}, 404
    

    def add_item(self, data):
        # Write-Around: Write directly to the database and invalidate the cache entry
        # This particular strategy is going to be most performant in instances where data is only written once and not updated.
        # The data is read very infrequently or not at all.
        item = Item(name=data['name'], description=data['description'])
        self.db.session.add(item)
        self.db.session.commit()
        # Invalidate cache or add to cache
        self.cache.delete(data['name'])
        self.logger.info("write-around ==> add_item: Cache invalidated!")
        # OR
        # Note: If the data is accessed very frequently and the overhead of regenerating the data in the cache is significant,
        # it may be better to update the cache with the new data. However, this could slow down the write operation and is not
        # suitable for write-intensive applications.
        # self.cache.set(data['name'], json.dumps({'name': item.name, 'description': item.description}))
        # self.logger.info("write-around ==> add_item: Cache updated!")
        return {'message': 'Item added'}, 201
    

    def update_item(self, data):
        item = Item.query.filter_by(name=data['name']).first()
        if item:
            item.description = data['description']
            self.db.session.commit()
            # Invalidate cache or add to cache
            self.cache.delete(data['name'])
            self.logger.info("write-around ==> update_item: Cache invalidated!")
            # self.cache.setex(data['name'], 3600, json.dumps({'name': item.name, 'description': item.description}))
            # self.logger.info("write-around ==> update_item: Cache updated!")
            return {'message': 'Item updated'}, 200
        return {'error': 'Item not found'}, 404