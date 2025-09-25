#!/usr/bin/env python3
"""
Module for Basic Authentication.

This module defines the `BasicAuth` class, which provides
methods for handling basic authentication.
"""

from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth.

    This class is responsible for handling basic authentication mechanisms.
    It provides methods to extract credentials from requests and retrieve
    user objects based on those credentials.
    """

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """
        Returns the User instance based on their email and password.

        This method checks for the validity of the provided email and password,
        searches for a user with the given email, and then verifies
        if the provided password matches the user's stored password.

        Args:
            user_email (str): The email of the user to authenticate.
            user_pwd (str): The password of the user to authenticate.

        Returns:
            TypeVar('User'): The `User` instance if the credentials are valid,
                             otherwise `None`. Returns `None` if `user_email`
                             or `user_pwd` are not strings, if no user is found
                             with the email, or if the password is incorrect.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        if not users:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None
