from typing import List
from datastructs import Smit
from . import pack2, pack
import hashlib


def _checksum(data: List[Smit], size: int) -> List[Smit]:
    payload = pack.decode(data)
    h = int.from_bytes(hashlib.sha1(str(payload).encode()).digest(), byteorder="big")
    return pack.encode(h, l=size)


def encode(n: int, checksum_size: int = 5) -> List[Smit]:
    payload = pack2.encode(n)
    return payload + _checksum(payload, checksum_size)


def decode(smits: List[Smit], checksum_size: int = 5) -> int:
    if len(smits) <= checksum_size:
        raise ValueError()
    payload = smits[:-checksum_size]
    redundancy = smits[-checksum_size:]
    if redundancy != _checksum(payload, checksum_size):
        raise ValueError()
    return pack2.decode(payload)
