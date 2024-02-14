#!/usr/bin/env python3
"""
This is the base module
"""
from datetime import datetime
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}


class Base:
    '''
    This is the base class
    '''

    def __init__(self, *args: list, **kwargs: dict):
        '''
        This is initialize a base instance
        '''
        s_class = str(self.__class__.__name__)
        if DATA.get(s_class) is None:
            DATA[s_class] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = self._parse_datetime(kwargs.get('created_at'))
        self.updated_at = self._parse_datetime(kwargs.get('updated_at'))

    def _parse_datetime(self, dt_str):
        '''
        This is parse datetime string to datetime object
        '''
        if dt_str is not None:
            return datetime.strptime(dt_str, TIMESTAMP_FORMAT)
        return datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        '''
        This is equality
        '''
        if type(self) != type(other):
            return False
        return self.id == other.id

    def to_json(self, for_serialization: bool = False) -> dict:
        '''
        This is convert the object to a JSON dictionary
        '''
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key[0] == '_':
                continue
            if isinstance(value, datetime):
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                result[key] = value
        return result

    @classmethod
    def load_from_file(cls):
        '''
        This load all objects from file
        '''
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        DATA[s_class] = {}
        if not path.exists(file_path):
            return

        with open(file_path, 'r') as f:
            objs_json = json.load(f)
            for obj_id, obj_json in objs_json.items():
                DATA[s_class][obj_id] = cls(**obj_json)

    @classmethod
    def save_to_file(cls):
        '''
        This saves all objects to file
        '''
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        objs_json = {
            obj_id: obj.to_json(True) for obj_id, obj in DATA[s_class].items()}
        with open(file_path, 'w') as f:
            json.dump(objs_json, f)

    def save(self):
        '''
        This saves current object
        '''
        s_class = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DATA[s_class][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        '''
        This removes object
        '''
        s_class = self.__class__.__name__
        if DATA[s_class].get(self.id) is not None:
            del DATA[s_class][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        '''
        This counts all objects in class
        '''
        s_class = cls.__name__
        return len(DATA[s_class])

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        '''
        Return all objects
        '''
        return cls.search()

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        '''
        This returns one object by ID
        '''
        s_class = cls.__name__
        return DATA[s_class].get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        '''
        This search all objects with matching attributes
        '''
        s_class = cls.__name__

        def _search(obj):
            if not attributes:
                return True
            return all(getattr(obj, k) == v for k, v in attributes.items())

        return list(filter(_search, DATA[s_class].values())))
