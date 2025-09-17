#!/usr/bin/env python3
"""
Basic Authentication module.
"""
import base64
from api.v1.auth.auth import Auth
from typing import Tuple, TypeVar


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth.
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str
    ) -> str:
        """
        Extracts the Base64 part of the Authorization header
        for a Basic Authentication.

        Args:
            authorization_header (str): The value of the Authorization header.

        Returns:
            str: The Base64 encoded part of the header, or None if invalid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
    ) -> str:
        """
        Decodes a Base64 string.

        Args:
            base64_authorization_header (str): The Base64 encoded string.

        Returns:
            str: The decoded string in UTF-8, or None if decoding fails.
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
    ) -> Tuple[str, str]:
        """
        Extracts user email and password from the decoded header string.

        Args:
            decoded_base64_authorization_header (str): The decoded
                credential string ("<email>:<password>").

        Returns:
            Tuple[str, str]: A tuple of (email, password), or (None, None)
                             if the string is invalid.
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
            self,
            user_email: str,
            user_pwd: str
    ) -> TypeVar('User'):
        """
        Returns the User instance based on his email and password.

        Args:
            user_email (str): The email of the user to retrieve.
            user_pwd (str): The password of the user.

        Returns:
            The User object if found and password is valid, otherwise None.
        """
        from models.user import User

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

        user = users[0]
        if user.is_valid_password(user_pwd):
            return user

        return None
