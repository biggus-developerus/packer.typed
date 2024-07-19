__all__ = ("Float",)

import struct

from .base import (
    TypeDescriptor,
)


class Float(TypeDescriptor):
    __data_size__: int = 4

    @classmethod
    def pack(cls, val: float) -> bytes:
        return struct.pack("f", val)

    @classmethod
    def unpack(cls, data: bytearray) -> tuple[int, int]:
        return cls.__data_size__, struct.unpack("f", data[: cls.__data_size__])[0]
