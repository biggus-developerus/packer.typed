# packer.typed
[![PyPI version](https://img.shields.io/pypi/v/packer.typed.svg?style=flat-square)](https://pypi.org/project/packer.typed/)
[![Python versions](https://img.shields.io/pypi/pyversions/packer.typed.svg?style=flat-square)](https://pypi.org/project/packer.typed/)

A modern library that simplifies packing and unpacking to a whole other level.

## Usage
### Basic Usage
```python
from packer import packable, Pack
from packer.pack_types import int_types as ints

@packable
@dataclass
class SimpleStruct:
    int32_member: Pack[ints.Int["L4"]]
    int8_member: Pack[ints.Int["L2"]]

s = SimpleStruct(3, 2)
s.pack() # bytearray(b'\x03\x00\x00\x00\x02\x00')
```

## Hacks
### Getting type hints back
```python
@packable
class SimpleStruct:
    int32_member: Pack[Int["L4"]]
    int8_member: Pack[Int["L2"]]

    def __init__(self) -> None:
        self.int32_member: int
        self.int8_member: int

# ----------------
# with dataclasses

@packable
@dataclass
class SimpleStruct:
    int32_member: Pack[Int["L4"]]
    int8_member: Pack[Int["L2"]]

    def __post_init__(self) -> None:
        self.int32_member: int
        self.int8_member: int
```