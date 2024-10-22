# packer.typed
[![PyPI version](https://img.shields.io/pypi/v/packer.typed.svg?style=flat-square)](https://pypi.org/project/packer.typed/)
[![Python versions](https://img.shields.io/pypi/pyversions/packer.typed.svg?style=flat-square)](https://pypi.org/project/packer.typed/)

A modern library that simplifies packing and unpacking to a whole other level.

## Usage
### Basic Usage
```python
from packer import (
    Pack, 
    OptionalPack,
    packable, 
    int32, 
    int8, 
    float,
)

from dataclasses import dataclass

@packable
@dataclass
class SimpleStruct:
    int32_member: Pack[int32]
    int8_member: Pack[int8]
    float_member: OptionalPack[float]

s = SimpleStruct(3, 2, None)
s.pack() # bytearray(b'\x03\x00\x00\x00\x02\x00')
```