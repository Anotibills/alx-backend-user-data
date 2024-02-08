#!/usr/bin/env python3
"""
Implement a function that expects one string argument and returns a salted
Implement a function that expects 2 arguments and returns a boolean
"""
import bcrypt
from typing import Union


def hash_password(password: str) -> bytes:
    """
    Hashes the given password string using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if a password matches its hashed counterpart using bcrypt.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The password to check.

    Returns:
        bool: True if the password matches its hash, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
