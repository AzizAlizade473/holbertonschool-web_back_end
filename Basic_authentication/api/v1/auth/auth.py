#!/usr/bin/env python3
"""
Module for authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Manages API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a path requires authentication.
        For now, this method returns False.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Gets the authorization header from the request.
        For now, this method returns None.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Gets the current user from the request.
        For now, this method returns None.
        """
        return None
