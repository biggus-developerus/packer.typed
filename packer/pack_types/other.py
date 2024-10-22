__all__ = ("AllData",)

from packer.protocols import (
    TypeDescriptor,
)


class _AllData(TypeDescriptor):
    _size: int = 0

    @classmethod
    def pack(cls, val: bytes) -> bytes:
        return val

    @classmethod
    def unpack(cls, data: bytes) -> bytes:
        return data


class AllData(bytes, _AllData): ...
