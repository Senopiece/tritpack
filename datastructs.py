from typing import Any


class Smit:
    _n: int

    def __init__(self, n: int):
        assert 0 <= n < 7
        self._n = n

    @property
    def value(self):
        return self._n

    def __hash__(self) -> int:
        return self._n

    def __repr__(self) -> str:
        return f"smit.{self._n}"

    def __eq__(self, other: Any):
        return isinstance(other, Smit) and self._n == other._n


class Octet:
    _n: int

    def __init__(self, n: int):
        assert 0 <= n < 8
        self._n = n

    @property
    def value(self):
        return self._n

    def __hash__(self) -> int:
        return self._n

    def __repr__(self) -> str:
        return f"octet.{self._n}"

    def __eq__(self, other: Any):
        return isinstance(other, Octet) and self._n == other._n
