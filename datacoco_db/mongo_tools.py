"""
    MongoInteraction
"""


from pymongo import MongoClient


class MongoInteraction:

    def __init__(self, host, database, user, password, port=27017):
        client = MongoClient(host, username=user, password=password)
        self.db = client[database]

    def fetch(self, collection, query=None):
        res = self.db[collection].find(query)
        for x in res:
            yield x

    def __str__(self):
        return self.__class__.__name__
