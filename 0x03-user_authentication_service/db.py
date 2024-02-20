#!/usr/bin/env python33
"""
This is the module on database
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar
from user import Base, User

DATA = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:
    '''
    This is the class to interact with the database.
    '''

    def __init__(self):
        '''
        This initializes database connection and create necessary tables.
        '''
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        '''
        This provides property to access the database session.
        '''
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''
        This adds a new user to the database.
        '''
        if not email or not hashed_password:
            return
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        '''
        This helps find a user by given criteria
        '''
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        '''
        This updates user information.
        '''
        user = self.find_user_by(id=user_id)
        for key, val in kwargs.items():
            if key not in DATA:
                raise ValueError("Invalid field for update")
            setattr(user, key, val)
        self._session.commit()
        return None
