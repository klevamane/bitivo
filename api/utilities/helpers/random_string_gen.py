"""Module for random string generator function."""
import random
from string import ascii_letters


def gen_string(length=6):
    """Helper method to generate a random string.

    :param length: the length of the string, defaults to 6
    :param length: int, optional
    """
    return ''.join(random.choices(ascii_letters, k=length))
