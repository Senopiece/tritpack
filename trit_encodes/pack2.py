from typing import List
from datastructs import Trit
from . import pack


def _count_ternary_digits(n: int):
    if n == 0:
        return 1
    res = 0
    while n != 0:
        n //= 3
        res += 1
    return res


def _s(trist_l: int):
    return (pow(3, trist_l) - 1) // 2 - 1


def encode(n: int) -> List[Trit]:
    d = _count_ternary_digits(n)
    s = _s(d)
    if s > n:
        d = d - 1
        s = _s(d)
    return pack.encode(n - s, l=d)


def decode(trits: List[Trit]) -> int:
    trist_l = len(trits)
    if trist_l == 0:
        raise ValueError()
    return pack.decode(trits) + _s(trist_l)
