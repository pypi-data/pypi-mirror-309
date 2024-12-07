import json
from typing import TypeVar

import pymongo

from RFML.interface.ICorpusAdaptor import ICorpusAdaptor

T = TypeVar("T")


class MongoDB_RND(ICorpusAdaptor[T]):
    def read(self, collection: str, query: str) -> {}:
        # Serialization
        json_data = json.dumps(T, default=lambda o: o.__dict__, indent=4)
        print(json_data)

        # Deserialization
        decoded_team = T(**json.loads(json_data))
        print(decoded_team)
        return T

    def empty(self, collection: str, query: {}) -> str:
        pass

    def is_empty(self, collection: str, query: {}) -> bool:
        pass

    def save(self, collection: str, value: {}) -> str:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["mydatabase"]
        mycol = mydb["customers"]

        mydict = {"name": "John", "address": "Highway 37"}

        x = mycol.insert_one(mydict)
        pass

    def delete(self, collection: str, query: {}) -> str:
        pass

    def update(self, collection: str, query: {}, value: {}) -> str:
        pass

        # class Student(object):
        #     def __init__(self, first_name: str, last_name: str):
        #         self.first_name = first_name
        #         self.last_name = last_name
        #
        # class Team(object):
        #     def __init__(self, students: List[Student]):
        #         self.students = students
        #
        # student1 = Student(first_name="Geeky", last_name="Guy")
        # student2 = Student(first_name="GFG", last_name="Rocks")
        # team = Team(students=[student1, student2])
        #
        # # Serialization
        # json_data = json.dumps(team, default=lambda o: o.__dict__, indent=4)
        # print(json_data)
        #
        # # Deserialization
        # decoded_team = Team(**json.loads(json_data))
        # print(decoded_team)
