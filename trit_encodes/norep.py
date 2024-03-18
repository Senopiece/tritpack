from typing import List
from datastructs import Trit

TCODES = {
    "0": Trit.A,
    "1": Trit.B,
    "2": Trit.C,
}

CMAP = {
    Trit.A: {
        "0": Trit.B,
        "1": Trit.C,
    },
    Trit.B: {
        "0": Trit.A,
        "1": Trit.C,
    },
    Trit.C: {
        "0": Trit.A,
        "1": Trit.B,
    },
}


def encode(n: int):
    assert n >= 0
    bits = bin(n)[2:]

    # special cases for 1's or 0's
    if len(bits) % 2 == 1:
        if all(bit == "0" for bit in bits):
            return [TCODES[t] for t in "01" * (len(bits) // 2) + "0"]

        if all(bit == "1" for bit in bits):
            return [TCODES[t] for t in "12" * (len(bits) // 2) + "1"]

    res: List[Trit] = [None] * len(bits)  # type: ignore

    # find 01
    infl = -1
    prev_bit = bits[-1]
    for i, curr_bit in enumerate(bits):
        if prev_bit + curr_bit == "01":
            infl = i
            break
        prev_bit = curr_bit

    # perform the encoding
    res[infl] = Trit.C
    for i in range(len(bits)):
        i = (i + infl + 1) % len(bits)
        curr_bit = bits[i]
        prev_trit = res[i - 1]
        res[i] = CMAP[prev_trit][curr_bit]

    return res


RCMAP = {
    Trit.A: {
        Trit.B: "0",
        Trit.C: "1",
    },
    Trit.B: {
        Trit.A: "0",
        Trit.C: "1",
    },
    Trit.C: {
        Trit.A: "0",
        Trit.B: "1",
    },
}


def decode(trits: list[Trit]):
    if len(trits) == 0:
        return ""

    # first check for the special cases of 1's and 0's
    if len(trits) % 2 == 1 and trits[0].value != Trit.C.value:
        key = trits[0].value
        odd = key + 1
        matched = True
        for i, curr_trit in enumerate(trits):
            if (i % 2 == 0 and curr_trit.value != key) or (
                i % 2 == 1 and curr_trit.value != odd
            ):
                matched = False
                break

        if matched:
            return "0" * len(trits) if key == 0 else "1" * len(trits)

    # check no repetitions and restore bits
    prev_trit = trits[-1]
    res = ""
    for curr_trit in trits:
        decoder = RCMAP[prev_trit]
        if curr_trit not in decoder:  # aka curr_trit != prev_trit
            raise ValueError()
        res += decoder[curr_trit]
        prev_trit = curr_trit

    return int(res, 2)
