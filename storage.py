__author__ = 'couldtt'

import pymongo
import time


class MongoStorage():
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        self.db = client.limitfree
        self.collection = self.db.books
        localtime = time.localtime(time.time())
        self.now_time = time.strftime('%Y%m%d%H', localtime)

    def save(self, platforms):
        today = {
            'time': self.now_time,
            'platforms': platforms
        }
        insert_id = self.collection.insert(today)
        if insert_id:
            return True

    def get_today(self):
        return self.collection.find_one({'time': self.now_time})