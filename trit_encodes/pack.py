from typing import List
from datastructs import Trit


def encode(n: int, l: int | None = None):
    if n == 0:
        return [Trit.A] if l is None else [Trit.A] * l
    trits: List[Trit] = []
    while True:
        n, remainder = divmod(n, 3)
        trits.append(Trit(remainder))
        if l is not None:
            l -= 1
            if l == 0:
                break
        elif n == 0:
            break
    return trits[::-1]


def decode(trits: List[Trit]) -> int:
    n = 0
    for trit in trits:
        n = n * 3 + trit.value
    return n
