__all__ = ("Sized",)

from typing import Self


class SizedMeta(type):
    def __getitem__(cls, size: int) -> Self:
        return type(f"SIZE{size}{cls.__name__}", (cls,), {"_size": size})


# TypeDescriptor
class _Sized(metaclass=SizedMeta):
    _size: int = 0  # setting size is done through __getitem__ (Sized[10])

    @classmethod
    def __pack__(cls, val: bytes) -> bytes:
        return val[: cls._size]

    @classmethod
    def __unpack__(cls, data: bytes) -> bytes:
        return data[: cls._size]


class Sized(bytes, _Sized): ...
