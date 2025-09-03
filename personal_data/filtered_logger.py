#!/usr/bin/env python3
"""
filtered_logger.py
"""
import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Returns the log message obfuscated.
    """
    pattern = f'({"|".join(fields)})=.*?{re.escape(separator)}'
    return re.sub(pattern, lambda m: f'{m.group(1)}={redaction}{separator}',
                  message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a log record and redacts sensitive information.
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                   record.getMessage(), self.SEPARATOR)
        return super().format(record)
