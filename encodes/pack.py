from typing import List
from datastructs import Smit


def encode(n: int, l: int | None = None):
    if n == 0:
        return [Smit(0)] if l is None else [Smit(0)] * l
    smits: List[Smit] = []
    while True:
        n, remainder = divmod(n, 7)
        smits.append(Smit(remainder))
        if l is not None:
            l -= 1
            if l == 0:
                break
        elif n == 0:
            break
    return smits[::-1]


def decode(smits: List[Smit]) -> int:
    n = 0
    for smit in smits:
        n = n * 7 + smit.value
    return n
