#!/usr/bin/env python3
"""
BasicAuth module for API authentication
"""
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """BasicAuth class for handling Basic authentication"""
    
    def extract_base64_authorization_header(self,
                                           authorization_header: str) -> str:
        """
        Extract the Base64 part of the Authorization header
        
        Args:
            authorization_header: The Authorization header string
            
        Returns:
            The Base64 encoded string or None
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]
    
    def decode_base64_authorization_header(self,
                                         base64_authorization_header: str
                                         ) -> str:
        """
        Decode a Base64 string
        
        Args:
            base64_authorization_header: The Base64 encoded string
            
        Returns:
            The decoded string or None
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
    
    def extract_user_credentials(self,
                                decoded_base64_authorization_header: str
                                ) -> (str, str):
        """
        Extract user email and password from the Base64 decoded value
        
        Args:
            decoded_base64_authorization_header: The decoded authorization
                                                   string
            
        Returns:
            Tuple of (email, password) or (None, None)
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        
        # Split only on the first colon to handle passwords with colons
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password
    
    def user_object_from_credentials(self,
                                    user_email: str,
                                    user_pwd: str) -> TypeVar('User'):
        """
        Return the User instance based on email and password
        
        Args:
            user_email: The user's email address
            user_pwd: The user's password
            
        Returns:
            The User instance if credentials are valid, None otherwise
        """
        # Check if user_email is None or not a string
        if user_email is None or not isinstance(user_email, str):
            return None
        
        # Check if user_pwd is None or not a string
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        
        # Search for users with the given email
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        
        # Check if no users found
        if not users or len(users) == 0:
            return None
        
        # Get the first user (should be unique by email)
        user = users[0]
        
        # Validate the password
        if not user.is_valid_password(user_pwd):
            return None
        
        # Return the user instance if all checks pass
        return user
