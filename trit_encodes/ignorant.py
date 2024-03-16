from datastructs import Trit


def encode(bits: str) -> list[Trit]:
    res = [None] * len(bits)
    for i, bit in enumerate(bits):
        res[i] = Trit.A if bit == "0" else Trit.B  # type: ignore
    return res  # type: ignore


def decode(trits: list[Trit]):
    if Trit.C in trits:
        raise ValueError()
    return "".join("0" if trit.value == Trit.A.value else "1" for trit in trits)
