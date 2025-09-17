#!/usr/bin/env python3
"""
BasicAuth class with user_object_from_credentials
"""
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic Authentication"""

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
        except Exception:
            return None

        if not users or len(users) == 0:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None
