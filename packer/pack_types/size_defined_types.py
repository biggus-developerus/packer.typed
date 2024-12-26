__all__ = ("Sized",)


class SizedMeta(type):
    def __getitem__(cls, size: int) -> type:
        return type(f"SIZE{size}{cls.__name__}", (cls,), {"_size": size})


# TypeDescriptor
class _Sized(metaclass=SizedMeta):
    _size: int = 0  # setting size is done through __getitem__ (Sized[10])

    @classmethod
    def pack(cls, val: bytes) -> bytes:
        return val[: cls._size]

    @classmethod
    def unpack(cls, data: bytes) -> bytes:
        return data[: cls._size]


class Sized(bytes, _Sized): ...  # type: ignore
