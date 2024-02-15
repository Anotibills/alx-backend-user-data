#!/usr/bin/env python3
"""
This is the Basic Authorization module
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import Optional


class BasicAuth(Auth):
    '''
    This is the class on Basic Authentication
    '''

    @staticmethod
    def extract_base64_authorization_header(
            authorization_header: str) -> Optional[str]:
        '''
        This returns Base64 part of Authorization header
        '''
        if authorization_header and isinstance(authorization_header, str) \
                and authorization_header.startswith("Basic "):
            return authorization_header[6:]

    @staticmethod
    def decode_base64_authorization_header(
            base64_authorization_header: str) -> Optional[str]:
        '''
        This returns decoded value of base64_authorization_header
        '''
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    @staticmethod
    def extract_user_credentials(
            decoded_base64_authorization_header: str) -> Optional[tuple]:
        '''
        This returns user email and password from decoded Base64
        '''
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None
        if ":" not in decoded_base64_authorization_header:
            return None
        return decoded_base64_authorization_header.split(':', 1)

    @staticmethod
    def user_object_from_credentials(
            user_email: str, user_pwd: str) -> Optional[User]:
        '''
        This returns User instance based on email and password
        '''
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None
        return None

    def current_user(self, request=None) -> Optional[User]:
        '''
        This overrides Auth and retrieves User instance for request
        '''
        auth_header = self.authorization_header(request)
        b64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(b64_header)
        user_creds = self.extract_user_credentials(decoded_header)
        if user_creds:
            return self.user_object_from_credentials(*user_creds)
        return None
