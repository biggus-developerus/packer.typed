__all__ = (  # sob..
    "int8",
    "int16",
    "int32",
    "int64",
    "uint8",
    "uint16",
    "uint32",
    "uint64",
    "float",
    "double",
)

from typing import Type

from .float_types import *
from .int_types import *

int8 = Type[Int["L2"]]
int16 = Type[Int["L2"]]
int32 = Type[Int["L4"]]
int64 = Type[Int["L8"]]

uint8 = Type[UInt["L1"]]
uint16 = Type[UInt["L2"]]
uint32 = Type[UInt["L4"]]
uint64 = Type[UInt["L8"]]

float = Type[Float[4]]
double = Type[Float[8]]
