
import json
from cache_aside import CacheAside
from models import Item
from read_through_cache import ReadThroughCache
from write_around_cache import WriteAroundCache
from write_through_cache import WriteThroughCache



class APIController:

    def __init__(self, db, cache, logger):
        self.db = db
        self.cache = cache
        self.logger = logger
        self.cac = CacheAside(cache, logger)
        self.rtc = ReadThroughCache(cache, logger)
        self.wtc = WriteThroughCache(db, cache, logger)
        self.wac = WriteAroundCache(db, cache, logger)


    def read_through_get_item(self, name):
        item = self.rtc.get_data(name)
        if item:
            return item, 200
        return {'error': 'Item not found'}, 404

    def cache_aside_get_item(self, name):
        # Check cache first
        item = self.cac.get_data(name)
        if item:
            return item, 200
        
        # Cache miss, query database
        self.logger.info("cache-aside ==> get_item: Cache miss!")
        item = Item.query.filter_by(name=name).first()
        
        # update cache
        if item:
            # cahce for 1 hour
            data = {'name': item.name, 'description': item.description}
            self.cac.set_data(item.name, json.dumps(data))
            self.logger.info("cache-aside ==> get_item: Cache updated!")
            return data, 200
        
        return {'error': 'Item not found'}, 404
    
    def add_item_wt(self, data):
        self.wtc.add_data(data)
        return {'message': 'Item added'}, 201

    def add_item_wa(self, data):
        self.wac.add_data(data)
        return {'message': 'Item added'}, 201
        
    
