# coding: utf-8

from ksupk import singleton_decorator, restore_json, save_json
from threading import Lock
import os


@singleton_decorator
class DB:
    def __init__(self, path: str):
        self.__lock = Lock()
        self.__path = path
        self.__classes_num = 3

        if not os.path.isfile(path):
            self.create_new(path)
        self.db = restore_json(path)

    def flush(self):
        with self.__lock:
            save_json(self.__path, self.db)

    def update(self, _id: int, hits: list):
        self.db["classes_hits"][str(_id)] = hits
        self.db["current"] = _id
        self.flush()

    def hits(self, _id: int) -> list:
        id_str = str(_id)
        if id_str in self.db["classes_hits"]:
            return self.db["classes_hits"][id_str]
        else:
            return [0]*self.__classes_num

    def current(self) -> int:
        return self.db["current"]

    def create_new(self, path: str):
        d = {
            "current": 1,
            "classes_hits": {}
        }
        self.db = d
        self.flush()
