#!/usr/bin/env python3
""" User module
"""
from models.base_model import BaseModel


class User(BaseModel):
    """User class that inherits from BaseModel"""
    def __init__(self, *args: list, **kwargs: dict):
        """Initialize User"""
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self._password = kwargs.get('password')

    @property
    def password(self) -> str:
        """Return the hashed password"""
        return self._password

    @password.setter
    def password(self, pwd: str):
        """Set password using hash"""
        from bcrypt import hashpw, gensalt
        if pwd is None:
            self._password = None
        else:
            self._password = hashpw(pwd.encode(), gensalt()).decode()

    def is_valid_password(self, pwd: str) -> bool:
        """Check if a password is valid"""
        from bcrypt import checkpw
        if pwd is None or self._password is None:
            return False
        return checkpw(pwd.encode(), self._password.encode())

    def display_name(self) -> str:
        """Return a display name for the user"""
        return "{} {}".format(self.first_name, self.last_name)

