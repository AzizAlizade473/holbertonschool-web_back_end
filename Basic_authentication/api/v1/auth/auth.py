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
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        normalized_path = path if path.endswith('/') else path + '/'
        
        if normalized_path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Gets the authorization header from the request.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Gets the current user from the request.
        """
        return None
