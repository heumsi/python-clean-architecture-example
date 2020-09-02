from typing import List

from rentomatic.domain.entities.room import Room
from rentomatic.domain.interfaces.repository import Repository


class MemRepo(Repository):
    def __init__(self, data: List[dict]) -> None:
        self.data = data

    def list(self, filters: dict = None) -> List[Room]:
        result = [Room.from_dict(i) for i in self.data]

        if filters is None:
            return result

        if "code__eq" in filters:
            result = [r for r in result if r.code == filters["code__eq"]]
        if "price__eq" in filters:
            result = [r for r in result if r.price == int(filters["price__eq"])]
        if "price__lt" in filters:
            result = [r for r in result if r.price < int(filters["price__lt"])]
        if "price__gt" in filters:
            result = [r for r in result if r.price > int(filters["price__gt"])]

        return result


""" usage example
    room1 = {
        "code": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
        "size": 215,
        "price": 39,
        "longitude": -0.09998975,
        "latitude": 51.75436293,
    }
    room2 = {
        "code": "fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a",
        "size": 405,
        "price": 66,
        "longitude": 0.18228006,
        "latitude": 51.74640997,
    }
    room3 = {
        "code": "913694c6-435a-4366-ba0d-da5334a611b2",
        "size": 56,
        "price": 60,
        "longitude": 0.27891577,
        "latitude": 51.45994069,
    }
    
    repo = MemRepo([room1, room2, room3])
"""
