#!/usr/bin/env python3
"""
Takes a string k and an int or float v, and returns a tuple.
"""


from typing import Union, Tuple

def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    The first element is k, and the second element is the square of v as a float.
    """
    return (k, float(v ** 2))
