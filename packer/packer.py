__all__ = ("packable",)

from typing import (
    Callable,
    Protocol,
    Self,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from ._types import *


class PackableProtocol(Protocol):
    _min_size: int
    _packing_data: list[tuple[str, Type, bool, Callable, Callable]]

    def pack(self) -> tuple[int, bytearray]: ...
    def unpack(self, data: bytearray) -> tuple[int, bool]: ...


class Packer:
    def __new__(cls, *args, **kwargs) -> Self:
        instance = super().__new__(cls)
        if getattr(cls, "_packing_data", None):
            return instance

        # attr name, attr_type, is_optional, packer, unpacker
        cls._packing_data = []
        cls._min_size = 0

        type_hints = get_type_hints(instance).items()
        type_hints_list = list(type_hints)

        hint_count = len(type_hints)

        for i, j in enumerate(type_hints):
            attr, attr_type = j
            origin = get_origin(attr_type)
            inner_type = get_args(attr_type)[0]

            next_attr = type_hints_list[i + 1 if i + 1 < hint_count else i][0]
            next_origin = get_origin(type_hints_list[i + 1 if i + 1 < hint_count else i][1])

            if not origin or origin not in {Pack, OptionalPack}:
                continue

            if not issubclass(inner_type, TypeDescriptor):
                raise ValueError(
                    f"The type corresponding with the attribute '{attr}' is marked as Pack but does not subclass TypeDescriptor."
                )

            optional = True
            if not origin is OptionalPack:
                optional = False
                cls._min_size += inner_type.__data_size__

            if optional and not next_origin is OptionalPack:
                raise ValueError(
                    f"{attr} ({origin}) is followed by {next_attr} ({next_origin}) which is not optional. "
                )

            packer, unpacker = inner_type.pack, inner_type.unpack
            cls._packing_data.append((attr, inner_type, optional, packer, unpacker))

        return instance

    def pack(self) -> bytearray:
        data = bytearray()

        for attr, attr_type, optional, packer, _ in self._packing_data:
            val = getattr(self, attr, None)

            if val is None and not optional:
                raise ValueError(
                    f"The value of {attr} cannot be None as it's not optional ({attr_type})"
                )

            if val is None and optional:  # just break cuz... laikeee???
                # TODO: Debug print to inform the user
                # that we broke (my money up doe on skibidi)
                # out of the loop and will no longer pack the remaining attrs.
                break

            data += packer(val)

        return data

    def unpack(self, data: bytearray) -> tuple[int, bool]:
        offset = 0
        data_len = len(data)

        if data_len < self._min_size:
            raise ValueError(
                f"Got data of length {data_len} and expected data of length >= {self._min_size}"
            )

        for attr, attr_type, optional, _, unpacker in self._packing_data:
            if offset >= data_len and optional:
                break

            val = unpacker(data[offset:])
            offset += attr_type.__data_size__
            setattr(self, attr, val)

        return offset, True


T = TypeVar("T")


def packable(
    cls: Type[T],
) -> Union[Type[T], Type[PackableProtocol]]:  # I mean... got better ideas??
    class ExtendedCls(cls, Packer): ...

    return ExtendedCls