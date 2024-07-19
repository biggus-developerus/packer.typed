__all__ = (
    "TypeDescriptor",
    "Pack",
    "OptionalPack",
)

from typing import (
    Generic,
    TypeVar,
)

T = TypeVar("T")


class TypeDescriptor:
    __data_size__ = 0

    @classmethod
    def pack(cls, _: T) -> bytes:
        raise NotImplementedError

    @classmethod
    def unpack(cls, _: bytearray) -> int:
        raise NotImplementedError


class Pack(Generic[T]): ...


class OptionalPack(Generic[T]): ...
