# packer.typed
[![PyPI version](https://img.shields.io/pypi/v/packer.typed.svg?style=flat-square)](https://pypi.org/project/packer.typed/)
[![Python versions](https://img.shields.io/pypi/pyversions/packer.typed.svg?style=flat-square)](https://pypi.org/project/packer.typed/)

A modern library that simplifies packing and unpacking to a whole other level.

## Usage
### Basic Usage
```py
from packer import Int8, Pack
from dataclasses import dataclass

@packable
@dataclass
class SimpleStruct:
    test1: Pack[Int8]
    test2: Pack[Int8]

test = SimpleStruct(1, 2)
test.pack() # \x01\x02
```
### Creating & Using custom types
```py
from packer import TypeDescriptor, packable, Pack, OptionalPack
from dataclasses import dataclass

class LengthPrefixedStr(TypeDescriptor):
    __data_size__: int = 2

    @classmethod
    def pack(cls, val: str) -> bytes:
        return int.to_bytes(len((enc := val.encode())), 2, "little") + enc

    @classmethod
    def unpack(cls, data: bytearray) -> tuple[int, str]:
        str_len = int.from_bytes(data[:2], "little")
        return str_len + 2, data[2 : 2 + str_len].decode()


@packable
@dataclass
class CustomTypesStruct:
    test1: Pack[LengthPrefixedStr]
    test2: OptionalPack[LengthPrefixedStr] = None

test = CustomTypesStruct("hi")
test.pack() # b"\x02\x00hi"

test.test2 = "hi2"
test.pack() #b"\x02\x00hi\x03\x00hi2"
```

## Notes
#### If you're going to use this with a dataclass then be prepared to lose object attr typehints. A simple workaround is to declare object attributes with the types like the following:
```py
@packable
@dataclass
class SimpleStruct:
    id: Pack[Int32] = 0
    val: OptionalPack[Float] = None

    def __post_init__(self) -> None:
        self.id: int
        self.val: float | None
```
---
