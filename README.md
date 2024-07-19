# packer.typed
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