#!/usr/bin/env python3
"""
Takes a float multiplier and returns a function that multiplies a float by the multiplier.
"""


from typing import Callable

def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    Takes a float multiplier.
    """
    def multiplier_function(value: float) -> float:
        return value * multiplier
    
    return multiplier_function
