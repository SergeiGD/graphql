from typing import Protocol


class SupportsId(Protocol):
    id: int


class SupportsName(Protocol):
    name: str

