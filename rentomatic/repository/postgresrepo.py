from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from rentomatic.domain.entities import room
from rentomatic.domain.interfaces.repository import Repository
from rentomatic.repository import postgres_objects


class PostgresRepo(Repository):
    def __init__(self, connection_data: dict) -> None:
        connection_string = "postgresql+psycopg2://{}:{}@{}/{}".format(
            connection_data["user"], connection_data["password"], connection_data["host"], connection_data["dbname"]
        )
        self.engine = create_engine(connection_string)
        postgres_objects.Base.metadata.bind = self.engine

    def _create_room_objects(self, results: List[postgres_objects.Room]) -> List[room.Room]:
        return [
            room.Room(code=q.code, size=q.size, price=q.price, latitude=q.latitude, longitude=q.longitude)
            for q in results
        ]

    def list(self, filters: dict = None) -> List[room.Room]:
        DBSession = sessionmaker(bind=self.engine)

        session = DBSession()
        query = session.query(postgres_objects.Room)
        if filters is None:
            return self._create_room_objects(query.all())
        if "code__eq" in filters:
            query = query.filter(postgres_objects.Room.code == filters["code__eq"])
        if "price__eq" in filters:
            query = query.filter(postgres_objects.Room.price == filters["price__eq"])
        if "price__lt" in filters:
            query = query.filter(postgres_objects.Room.price < filters["price__lt"])
        if "price__gt" in filters:
            query = query.filter(postgres_objects.Room.price > filters["price__gt"])
        return self._create_room_objects(query.all())


""" usage example 
    repo = PostgresRepo({"dbname": "rentomaticdb", "user": "postgres", "password": "rentomaticdb", "host": "localhost"})
"""
