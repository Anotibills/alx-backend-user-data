#!/usr/bin/env python3
"""
This is the API module on Session Expiration
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    '''
    This is the class of Session Expiration
    '''

    def __init__(self):
        '''
        This overrides the initial method
        '''
        super().__init__()  # Call parent class constructor

        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        '''
        This creates a Session ID for user_id
        '''
        session_id = super().create_session(user_id)
        if session_id:
            session_dictionary = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
            self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''
        This returns User ID based on Session ID
        '''
        if session_id is None or not isinstance(session_id, str):
            return None

        session_dict = self.user_id_by_session_id.get(session_id)

        if session_dict is None or 'created_at' not in session_dict:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_time = session_dict.get('created_at')
        session_elapsed = timedelta(seconds=self.session_duration)

        if created_time + session_elapsed < datetime.now():
            return None
        else:
            return session_dict.get('user_id')
