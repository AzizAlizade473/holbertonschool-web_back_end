#!/usr/bin/env python3
"""
Encrypts a password using bcrypt.
"""
import bcrypt
from typing import Union


def hash_password(password: str) -> bytes:
    """
    Hashes a password using a randomly generated salt.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
