#!/usr/bin/env python3
"""Module for Basic Authentication.

This module provides the `BasicAuth` class for handling
basic authentication in the API.
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar, Optional


class BasicAuth(Auth):
    """BasicAuth class for basic authentication.

    This class inherits from `Auth` and provides an implementation
    for a basic authentication system based on user credentials.
    """

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
    ) -> Optional[TypeVar('User')]:
        """Retrieves a User instance based on email and password.

        This method validates the user's credentials against the
        stored user data.

        Args:
            user_email (str): The email of the user.
            user_pwd (str): The password of the user.

        Returns:
            Optional[TypeVar('User')]: The User instance if the credentials
            are valid, otherwise None. It returns None if `user_email` or
            `user_pwd` are not strings, if no user is found with the email,
            or if the password is incorrect.
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
