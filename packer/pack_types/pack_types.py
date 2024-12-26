__all__ = (  # sob..
    "int8",
    "int16",
    "int32",
    "int64",
    "uint8",
    "uint16",
    "uint32",
    "uint64",
    "float32",
    "float64",
)

from typing import Type

from .float_types import *
from .int_types import *

int8 = Type[Int["L1"]]  # type: ignore
int16 = Type[Int["L2"]]  # type: ignore
int32 = Type[Int["L4"]]  # type: ignore
int64 = Type[Int["L8"]]  # type: ignore

uint8 = Type[UInt["L1"]]  # type: ignore
uint16 = Type[UInt["L2"]]  # type: ignore
uint32 = Type[UInt["L4"]]  # type: ignore
uint64 = Type[UInt["L8"]]  # type: ignore

float32 = Type[Float[4]]  # type: ignore
float64 = Type[Float[8]]  # type: ignore
