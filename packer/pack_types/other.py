__all__ = ("AllData",)

from packer.protocols import (
    TypeDescriptor,
)


class _AllData(TypeDescriptor):
    _size: int = 0

    @classmethod
    def __pack__(cls, val: bytes) -> bytes:
        return val

    @classmethod
    def __unpack__(cls, data: bytes) -> bytes:
        return data


class AllData(bytes, _AllData): ...
