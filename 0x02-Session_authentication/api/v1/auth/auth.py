#!/usr/bin/env python3
"""
This is the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    '''
    The class that manages the API authentication
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
        This returns excluded path
        '''
        if not path or not excluded_paths or not excluded_paths:
            return True
        if not excluded_paths:
            return True
        if path[-1] != '/':
            path += '/'
        for p in excluded_paths:
            if p.endswith('*'):
                if path.startswith(p[:-1]):
                    return False
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        '''
        This authorize header check
        '''
        if request:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        This return current method
        '''
        return None
