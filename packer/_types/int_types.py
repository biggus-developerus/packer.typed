__all__ = ("Int64", "Int32", "Int16", "Int8")

import sys

from .base import (
    TypeDescriptor,
)

# TODO: Type options, where it's possible to do the following:
"""
@packable
@dataclass
class Test:
    test: Pack[Int32[False]] = 0
"""
# Where the False denotes whether it's a signed or unsigned int.
# This could be done with metaclasses and overriding __getitem__ 👍👍


class Int64(TypeDescriptor):
    __data_size__: int = 8

    @classmethod
    def pack(cls, val: int) -> bytes:
        return val.to_bytes(cls.__data_size__, sys.byteorder, signed=True)

    @classmethod
    def unpack(cls, data: bytearray) -> tuple[int, int]:
        return cls.__data_size__, int.from_bytes(
            data[: cls.__data_size__], sys.byteorder, signed=True
        )


class Int32(TypeDescriptor):
    __data_size__: int = 4

    @classmethod
    def pack(cls, val: int) -> bytes:
        return val.to_bytes(cls.__data_size__, sys.byteorder, signed=True)

    @classmethod
    def unpack(cls, data: bytearray) -> tuple[int, int]:
        return cls.__data_size__, int.from_bytes(
            data[: cls.__data_size__], sys.byteorder, signed=True
        )


class Int16(TypeDescriptor):
    __data_size__: int = 2

    @classmethod
    def pack(cls, val: int) -> bytes:
        return val.to_bytes(cls.__data_size__, sys.byteorder, signed=True)

    @classmethod
    def unpack(cls, data: bytearray) -> tuple[int, int]:
        return cls.__data_size__, int.from_bytes(
            data[: cls.__data_size__], sys.byteorder, signed=True
        )


class Int8(TypeDescriptor):
    __data_size__: int = 1

    @classmethod
    def pack(cls, val: int) -> bytes:
        return val.to_bytes(cls.__data_size__, sys.byteorder, signed=True)

    @classmethod
    def unpack(cls, data: bytearray) -> tuple[int, int]:
        return cls.__data_size__, int.from_bytes(
            data[: cls.__data_size__], sys.byteorder, signed=True
        )


class UInt32(TypeDescriptor):
    __data_size__: int = 4

    @classmethod
    def pack(cls, val: int) -> bytes:
        return val.to_bytes(cls.__data_size__, sys.byteorder)

    @classmethod
    def unpack(cls, data: bytearray) -> tuple[int, int]:
        return cls.__data_size__, int.from_bytes(data[: cls.__data_size__], sys.byteorder)


class UInt16(TypeDescriptor):
    __data_size__: int = 2

    @classmethod
    def pack(cls, val: int) -> bytes:
        return val.to_bytes(cls.__data_size__, sys.byteorder)

    @classmethod
    def unpack(cls, data: bytearray) -> tuple[int, int]:
        return cls.__data_size__, int.from_bytes(data[: cls.__data_size__], sys.byteorder)


class UInt8(TypeDescriptor):
    __data_size__: int = 1

    @classmethod
    def pack(cls, val: int) -> bytes:
        return val.to_bytes(cls.__data_size__, sys.byteorder)

    @classmethod
    def unpack(cls, data: bytearray) -> tuple[int, int]:
        return cls.__data_size__, int.from_bytes(data[: cls.__data_size__], sys.byteorder)
