#!/usr/bin/env python3
"""
This is the module on API authentication for the session
"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    '''
    This is the class of session Authentication
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''
        This creates a Session ID for user_id
        '''
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''
        This returns User ID based on Session ID
        '''
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        '''
        This returns a User instance based on cookie value
        '''
        session_id = self.session_cookie(request)
        if session_id:
            user_id = self.user_id_for_session_id(session_id)
            if user_id:
                return User.get(user_id)
        return None

    def destroy_session(self, request=None) -> bool:
        '''
        This deletes user session to logout
        '''
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id and session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
            return True

        return False
