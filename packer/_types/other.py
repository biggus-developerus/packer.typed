__all__ = ("AllData",)

from .base import (
    TypeDescriptor,
)


class AllData(TypeDescriptor):
    __data_size__: int = 0

    @classmethod
    def pack(cls, val: bytes) -> bytes:
        return val

    @classmethod
    def unpack(cls, data: bytearray) -> tuple[int, bytearray]:
        return len(data), data
