
import json
from models import Item

class CacheAsideController:

    def __init__(self, db, cache, logger):
        self.db = db
        self.cache = cache
        self.logger = logger


    def get_item(self, name):
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
            self.cache.set(name, json.dumps({'name': item.name, 'description': item.description}))
            self.logger.info("cache-aside ==> get_item: Cache updated!")
            return {'name': item.name, 'description': item.description}, 200
        return {'error': 'Item not found'}, 404
    

    def add_item(self, data):
        item = Item(name=data['name'], description=data['description'])
        self.db.session.add(item)
        self.db.session.commit()
        # Invalidate cache or add to cache
        self.cache.set(data['name'], json.dumps({'name': item.name, 'description': item.description}))
        self.logger.info("cache-aside ==> add_item: Cache updated!")
        return {'message': 'Item added'}, 201
    

    def update_item(self, data):
        item = Item.query.filter_by(name=data['name']).first()
        if item:
            item.description = data['description']
            self.db.session.commit()
            # Update cache with new data
            self.cache.set(data['name'], json.dumps({'name': item.name, 'description': item.description}))
            self.logger.info("cache-aside ==> update_item: Cache updated!")
            return {'message': 'Item updated'}, 200
        return {'error': 'Item not found'}, 404