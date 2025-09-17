#!/usr/bin/env python3
"""
Basic Authentication module
"""
from api.v1.auth.auth import Auth
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """
    Basic Authentication class that inherits from Auth.
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """
        Returns the Base64 part of the Authorization header
        for a Basic Authentication.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """
        Returns the decoded value of a Base64 string.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """
        Returns the user email and password
        from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)

        credentials = decoded_base64_authorization_header.split(":", 1)
        return (credentials[0], credentials[1])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on his email and password.

        Args:
            user_email (str): The email of the user to authenticate.
            user_pwd (str): The password of the user to authenticate.

        Returns:
            User: The User instance if the credentials are valid, otherwise None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        from models.user import User

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

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request by using Basic Auth.
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        base64_header = self.extract_base64_authorization_header(auth_header)
        if base64_header is None:
            return None

        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
