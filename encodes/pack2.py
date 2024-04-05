from typing import List
from datastructs import Smit
from . import pack


def _count_semiary_digits(n: int):
    if n == 0:
        return 1
    res = 0
    while n != 0:
        n //= 7
        res += 1
    return res


def _s(smits_l: int):
    return (pow(7, smits_l) - 1) // 6 - 1
    # return int('1' * (s - 1) + '0', 7)


def encode(n: int):
    d = _count_semiary_digits(n)
    s = _s(d)
    if s > n:
        d = d - 1
        s = _s(d)
    return pack.encode(n - s, l=d)


def decode(smits: List[Smit]) -> int:
    smits_l = len(smits)
    if smits_l == 0:
        raise ValueError()
    return pack.decode(smits) + _s(smits_l)
