"""Main module."""

import string
import random

def get_random_string(length=10, upper=False, digits=False):
    """Generate a random string of fixed length.

    Args:
        length (int, optional): The length of the string. Defaults to 10.
        upper (bool, optional): Whether to include uppercase letters. Defaults to False.
        digits (bool, optional): Whether to include digits. Defaults to False.

    Returns:
        str: The random string.
    """    
    letters = string.ascii_lowercase
    if upper:
        letters = letters + string.ascii_uppercase
    if digits:
        letters = letters + string.digits
    print(letters)
    return ''.join(random.choice(letters) for i in range(length))


def get_lucky_number(length=1):
    """generate a random number of fixed length.

    Args:
        length (int, optional): The length of the number. Defaults to 1.

    Returns:
        int: the random number.
    """    
    result = ''.join(random.choice(string.digits) for i in range(length))
    return int(result)
