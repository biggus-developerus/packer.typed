__all__ = (
    "Packable",
    "TypeDescriptor",
)

from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


@runtime_checkable
class Packable(Protocol):
    _size: int

    def pack(self) -> bytearray: ...
    def unpack(self, data: bytearray) -> bool: ...


@runtime_checkable
class TypeDescriptor(Protocol):
    _size: int

    @classmethod
    def pack(cls, val: Any) -> bytes | bytearray: ...
    @classmethod
    def unpack(cls, data: bytearray) -> Any: ...
