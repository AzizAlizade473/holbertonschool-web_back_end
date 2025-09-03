#!/usr/bin/env python3
"""
Validates a password against a hashed password.
"""
import bcrypt


def is_valid(password: str, hashed_password: bytes) -> bool:
    """
    Checks if a given password matches a hashed password.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
