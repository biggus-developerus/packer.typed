__all__ = (
    "Pack",
    "OptionalPack",
    "packable",
)

from dataclasses import (
    dataclass,
)
from typing import (
    Any,
    Optional,
    Self,
    Type,
    TypeVar,
    get_args,
    get_origin,
    get_type_hints,
)

from .exceptions import *
from .pack_types import (
    OptionalPack,
    Pack,
)
from .protocols import (
    Packable,
    TypeDescriptor,
)
from .utils import (
    create_pack_pair,
)


@dataclass
class PackData:
    attr_name: str
    offset: int
    type_descriptor: Type[Packable]
    optional: bool


def get_valid_type(attr_type: Type) -> Optional[Type[Packable]]:
    if not isinstance(attr_type, (Packable, TypeDescriptor)):
        inner_type = get_args(attr_type)
        if not inner_type:
            return None
        return get_valid_type(inner_type[0])
    return attr_type


class Packer(Packable):
    _packing_data: list[PackData]

    def __new__(cls, *args, **kwargs) -> Self:
        assert cls.__base__ is not None, "Base class cannot be None"

        instance = super().__new__(cls)

        if getattr(cls, "_packing_data", None):
            return instance

        cls._packing_data = []
        type_hints: list[tuple[str, Any]]

        try:
            _type_hints = get_type_hints(cls)
            if not _type_hints:
                raise PackerInvalidTypeHints(cls.__base__)
            type_hints = list(_type_hints.items())
        except TypeError:
            raise PackerInvalidTypeHints(cls.__base__)

        offset = 0
        last_origin = None

        for i in type_hints:
            attr = i[0]
            type_hint = i[1]

            origin = get_origin(type_hint)
            inner_types = get_args(type_hint)

            if not inner_types:
                continue

            inner_type = get_valid_type(inner_types[0])

            if origin not in {Pack, OptionalPack} or not inner_type:
                continue

            if last_origin == OptionalPack and origin == Pack:
                raise PackerException(
                    f"`{attr}` (non-optional) comes after `{type_hints[type_hints.index(i)-1][0]}` which is an optional member.",
                    cls.__base__,
                )

            cls._packing_data.append(PackData(attr, offset, inner_type, origin == OptionalPack))

            offset += inner_type._size
            last_origin = origin

        pack_pair = create_pack_pair(cls.__base__, cls._packing_data)

        setattr(cls, "pack", pack_pair[0])
        setattr(cls, "unpack", pack_pair[1])
        setattr(cls, "_size", offset)

        return instance

    def pack(self) -> bytearray: ...  # type: ignore
    def unpack(self, _: bytearray) -> bool: ...  # type: ignore


T = TypeVar("T")


def packable(cls: Type[T]) -> Type[T] | Type[Packable]:
    return type(f"{cls.__name__}Packable", (cls, Packer), {"__is_extended_packable__": True})
