from typing import Dict, List, Union, Tuple
import sympy

"""
Much thanks to claude.ai for editing and adding comments/docstrings
Code is otherwise original, by me
"""


def decompose_dict(factor_dict: Dict[int, int]) -> List[int]:
    """
    Converts a dictionary of factors and their counts into a list of individual factors.

    Args:
        factor_dict: Dictionary where keys are factors and values are their count/exponent

    Returns:
        List of individual factors, with each factor repeated according to its count

    Example:
        >>> decompose_dict({2: 2, 3: 1})
        [2, 2, 3]
    """
    if not isinstance(factor_dict, dict):
        raise TypeError("Input must be a dictionary")

    result = []
    for factor, count in factor_dict.items():
        if not isinstance(count, int) or count < 0:
            raise ValueError("Factor counts must be non-negative integers")
        result.extend([factor] * count)
    return result


def factor_check(initial_factor: Union[int, List[int]], attempt: int = 0) -> Union[Tuple[int, int], Tuple[int, tuple]]:
    """
    Checks if a number or list of factors can be decomposed into products less than 99.
    Used for optimizing pump pause durations.
    
    Args:
        initial_factor: Either an integer to factorize or a list of prime factors
        attempt: Internal parameter for tracking recursive attempts
    
    Returns:
        A tuple containing two elements where each is either an integer <= 99 or a nested tuple
        representing further factorization
    
    Raises:
        TypeError: If initial_factor is neither an int nor a list
        ValueError: If any factor is greater than 99
    """
    if isinstance(initial_factor, int):
        initial_factor = decompose_dict(sympy.factorint(initial_factor))
    elif not isinstance(initial_factor, list):
        raise TypeError("initial_factor must be an integer or list")

    if any(not isinstance(x, int) for x in initial_factor):
        raise TypeError("All factors must be integers")
    if any(x > 99 for x in initial_factor):
        return (0, 0)
    
    if len(initial_factor) == 1:
        return (0, 0)
    
    factor = initial_factor.copy()
    a = 0
    b = 0
    i = 0
    
    while i < len(factor):
        if i + 1 < len(factor) and factor[i] * factor[i + 1] < 99:
            factor[i + 1] = factor[i] * factor[i + 1]
            factor[i] = 1
            i += 1
        else:
            a = factor[i]
            factor[i] = 1
            i = len(factor)
    
    b = sympy.prod(factor)
    if b <= 99:
        return (a, b)
    return (a, factor_check(decompose_dict(sympy.factorint(b))))