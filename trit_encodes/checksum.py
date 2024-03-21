from typing import List
from datastructs import Trit
from . import pack2, pack
import hashlib


def checksum8(data: List[Trit]) -> List[Trit]:
    payload = pack.decode(data)
    h = int.from_bytes(hashlib.sha1(str(payload).encode()).digest())
    return pack.encode(h, l=8)


def encode(n: int) -> List[Trit]:
    payload = pack2.encode(n)
    return payload + checksum8(payload)


def decode(trits: List[Trit]) -> int:
    if len(trits) <= 8:
        raise ValueError()
    payload = trits[:-8]
    checksum = trits[-8:]
    if checksum != checksum8(payload):
        raise ValueError()
    return pack2.decode(payload)
