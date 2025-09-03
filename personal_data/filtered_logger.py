#!/usr/bin/env python3
from typing import List
import re

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    
    pattern = f'({"|".join(fields)})=.*?{re.escape(separator)}'
    return re.sub(pattern, lambda m: f'{m.group(1)}={redaction}{separator}', message)
