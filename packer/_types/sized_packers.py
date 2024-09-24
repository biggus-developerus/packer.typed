__all__ = ("SizedData",)

from typing import (
    Callable,
    Type,
)

from .base import (
    TypeDescriptor,
)


def _pack_sized_data_wrapper(size: int) -> Callable:
    def inner_packer(val: bytes) -> bytes:
        if (data_len := len(val)) < size:
            raise ValueError(
                f"Attempted to pack data of size {data_len}, expected data of size {size}."
            )
        return val

    return inner_packer


def _unpack_sized_data_wrapper(size: int) -> Callable:
    def inner_unpack(data: bytearray) -> tuple[int, bytearray]:
        return (size, data[:size])

    return inner_unpack


class SizedDataMeta(type):
    def __getitem__(cls, data_size: int) -> Type["SizedData"]:
        return type(
            f"{cls.__name__}({data_size})",
            (TypeDescriptor,),
            {
                "__data_size__": data_size,
                "pack": _pack_sized_data_wrapper(data_size),
                "unpack": _unpack_sized_data_wrapper(data_size),
            },
        )


class SizedData(metaclass=SizedDataMeta):
    def pack(val: bytes) -> bytes: ...
    def unpack(data: bytearray) -> tuple[int, bytearray]: ...
