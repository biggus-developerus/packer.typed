__all__ = ("Int32", "Int16", "Int8")

import sys

from .base import (
    TypeDescriptor,
)


class Int32(TypeDescriptor):
    __data_size__: int = 4

    @classmethod
    def pack(cls, val: int) -> bytes:
        return val.to_bytes(cls.__data_size__, sys.byteorder)

    @classmethod
    def unpack(cls, data: bytearray) -> tuple[int, int]:
        return cls.__data_size__, int.from_bytes(data[: cls.__data_size__], sys.byteorder)


class Int16(TypeDescriptor):
    __data_size__: int = 2

    @classmethod
    def pack(cls, val: int) -> bytes:
        return val.to_bytes(cls.__data_size__, sys.byteorder)

    @classmethod
    def unpack(cls, data: bytearray) -> tuple[int, int]:
        return cls.__data_size__, int.from_bytes(data[: cls.__data_size__], sys.byteorder)


class Int8(TypeDescriptor):
    __data_size__: int = 1

    @classmethod
    def pack(cls, val: int) -> bytes:
        return val.to_bytes(cls.__data_size__, sys.byteorder)

    @classmethod
    def unpack(cls, data: bytearray) -> tuple[int, int]:
        return cls.__data_size__, int.from_bytes(data[: cls.__data_size__], sys.byteorder)
