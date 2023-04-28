"""Main module."""

import string
import random

def get_random_string(length=10, upper=False, digits=False):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    if upper:
        letters = letters + string.ascii_uppercase
    if digits:
        letters = letters + string.digits
    print(letters)
    return ''.join(random.choice(letters) for i in range(length))


def get_lucky_number(length=1):
    """Generate a lucky number"""
    result = ''.join(random.choice(string.digits) for i in range(length))
    return int(result)
