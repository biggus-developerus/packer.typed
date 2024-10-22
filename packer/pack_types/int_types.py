__all__ = (
    "Int",
    "UInt",
)

from typing import (
    Literal,
    Self,
)

type INTS = Literal["L1", "L2", "L4", "L8", "B1", "B2", "B4", "B8"]


class IntMeta(type):
    def __getitem__(cls, size_and_order: INTS) -> Self:
        order = "little" if size_and_order[0].lower() == "l" else "big"
        size = int(size_and_order[1:])

        return type(
            f"{size_and_order[0]}{cls.__name__}{size * 8}", (cls,), {"_size": size, "_order": order}
        )


# TypeDescriptor
class _Int(metaclass=IntMeta):
    _size: int = 4
    _order: str = "little"
    _signed: bool = False

    @classmethod
    def __pack__(cls, val: int) -> bytes:
        return val.to_bytes(cls._size, cls._order, signed=cls._signed)

    @classmethod
    def __unpack__(cls, data: bytearray) -> int:
        return int.from_bytes(data[: cls._size], cls._order, signed=cls._signed)


class Int(_Int, int): ...


class UInt(_Int, int):
    _signed: bool = True
