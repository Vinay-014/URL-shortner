import random
import string
import re

def generate_short_code():
    """Generate a 6-character alphanumeric short code."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

def is_valid_url(url):
    """Validate URL format (starts with http(s):// and is well-formed)."""
    if not url:
        return False
    regex = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(regex, url))