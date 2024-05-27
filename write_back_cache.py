import json


class WriteBackCache:
    def __init__(self, cache_instance, queue, logger):
        self.cache = cache_instance
        self.queue = queue
        self.logger = logger

    def add_data(self, data):
        # Update cache
        self.cache.setex(data['name'], 3600, json.dumps(data))
        self.logger.info("write-back ==> add_item: Cache updated!")
        # Push data to queue
        self.queue.publish_message(json.dumps(data))
        return data
