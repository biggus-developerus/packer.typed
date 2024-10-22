__all__ = (
    "PackerException",
    "PackerInvalidTypeHints",
)

from typing import (
    Type,
    TypeVar,
)

T = TypeVar("T")


class PackerException(Exception):
    def __init__(self, msg: str, bad_cls: Type[T]):
        super().__init__(msg)
        self._bad_cls: Type[T] = bad_cls

    def __str__(self):
        return f"({self._bad_cls.__name__}) {super().__str__()}"


class PackerInvalidTypeHints(PackerException):
    def __init__(self, bad_cls: type[T]):
        super().__init__("Class does not have valid type hints.", bad_cls)
