__all__ = (
    "Pack",
    "OptionalPack",
)

from typing import (
    Annotated,
    TypeVar,
)

T = TypeVar("T")


type Pack[T] = Annotated[T, ""]
type OptionalPack[T] = Annotated[T, ""]

# TODO: ConditionalPack & RuntimePack (where sizes are determined in runtime (length prefixed data))
