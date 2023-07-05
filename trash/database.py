from typing import Any
from dataclasses import dataclass


class Settings:
    DATABASE_DRIVER = "sqlite"


ORM_MAPPINGS = {
    "CREATE_TABLE": {
        "sqlite": "CREATE TABLE IF NOT EXIST",
        "postgres": "CREATE TABLE",
    }
}


class DataMapper:
    def __init__(self, schema: object):
        self._shema = schema

    def _connect(self):
        self._session = None  # Connection string

    def create_table_if_not_exist(self):
        table_name = "".join((self._schema.__name__.lower(), "s"))
        _query = ORM_MAPPINGS[Settings.DATABASE_DRIVER]["CREATE_TABLE"]
        query = f"{_query} {table_name}"
        self._session.execute(query)

    def insert(self, payload: dict):
        ...


class Schema:
    def __init__(self):
        self._mapper = DataMapper(self)

    id: int

    def save(self):
        self._mapper.insert({self.username})

    def delete(self, id_: int):
        pass

    def get(self, key: str, value: Any):
        self._mapper.select(...)


@dataclass
class User(Schema):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str


@dataclass
class Request(Schema):
    title: str
    text: str
    visibility: bool
    user_id: int
    manager_id: int


@dataclass
class Message(Schema):
    text: str
    user_id: int
    request_id: int


john = User(
    id=1,
    username="john",
    email="john@email.com",
    password="27c06c2aeb517b7e71f4bfc8f1b2b36b",
)

john.save()