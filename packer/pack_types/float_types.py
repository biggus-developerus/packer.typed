__all__ = ("Float",)

import struct


class FloatMeta(type):
    def __getitem__(cls, size: int) -> type:
        size_str = "f" if size == 4 else "d"
        return type(f"{size_str}{cls.__name__}", (cls,), {"_size": size, "_size_str": size_str})


# TypeDescriptor
class _Float(metaclass=FloatMeta):
    _size_str: str = "f"
    _size: int = 4

    @classmethod
    def pack(cls, val: float) -> bytes:
        return struct.pack(cls._size_str, val)

    @classmethod
    def unpack(cls, data: bytes) -> float:
        return struct.unpack(cls._size_str, data)[0]


class Float(float, _Float): ...
