from typing import List

import pymongo

from rentomatic.domain.entities.room import Room
from rentomatic.domain.interfaces.repository import Repository


class MongoRepo(Repository):
    def __init__(self, connection_data: dict) -> None:
        client = pymongo.MongoClient(
            host=connection_data["host"],
            username=connection_data["user"],
            password=connection_data["password"],
            authSource="admin",
        )
        self.db = client[connection_data["dbname"]]

    def list(self, filters: dict = None) -> List[Room]:
        collection = self.db.rooms
        if filters is None:
            result = collection.find()
        else:
            mongo_filter = {}
        for key, value in filters.items():
            key, operator = key.split("__")
            filter_value = mongo_filter.get(key, {})
            if key == "price":
                value = int(value)
            filter_value["${}".format(operator)] = value
            mongo_filter[key] = filter_value
        result = collection.find(mongo_filter)
        return [Room.from_dict(d) for d in result]
