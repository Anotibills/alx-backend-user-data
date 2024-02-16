#!/usr/bin/env python3
"""
This is the module on Session Database Authentication
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from os import getenv


class SessionDBAuth(SessionExpAuth):
    '''
    This is the class of Session Database Authentication
    '''

    def create_session(self, user_id: str = None) -> str:
        '''
        This creates a Session ID for user_id
        '''
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = super().create_session(user_id)
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''
        This returns User ID based on Session ID
        '''
        if session_id is None or not isinstance(session_id, str):
            return None

        return user_id

    def destroy_session(self, request=None):
        '''
        This deletes user session to logout
        '''
        super().destroy_session(request)
