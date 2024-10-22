__all__ = (
    "Pack",
    "OptionalPack",
)

from enum import Enum
from typing import (
    Annotated,
    TypeVar,
)

T = TypeVar("T")


class PackType(Enum):
    NON_OPTIONAL = 0
    OPTIONAL = 1


type Pack[T] = Annotated[T, PackType.NON_OPTIONAL]
type OptionalPack[T] = Annotated[T, PackType.OPTIONAL]

# TODO: ConditionalPack?!
