#!/usr/bin/env python3
"""
Handles password encryption and validation.
"""
import bcrypt
from typing import Union


def hash_password(password: str) -> bytes:
    """
    Hashes a password using a randomly generated salt.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if a given password matches a hashed password.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
