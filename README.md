# packer.typed
[![PyPI version](https://img.shields.io/pypi/v/packer.typed.svg?style=flat-square)](https://pypi.org/project/packer.typed/)
[![Python versions](https://img.shields.io/pypi/pyversions/packer.typed.svg?style=flat-square)](https://pypi.org/project/packer.typed/)
![Pypi status](https://github.com/biggus-developerus/packer.typed/actions/workflows/upload.yml/badge.svg)
![Test status](https://github.com/biggus-developerus/packer.typed/actions/workflows/test.yml/badge.svg)

A modern library that simplifies packing and unpacking to a whole other level.

## Usage
### Basic Usage
```python
from dataclasses import dataclass
from packer import *

@packable
@dataclass
class SimpleStruct:
    int32_member: Pack[int32]
    int8_member: Pack[int8]
    float_member: OptionalPack[float32]

s = SimpleStruct(3, 2, None)
s.pack() # bytearray(b'\x03\x00\x00\x00\x02')

s.unpack(bytearray(b'\x01\x00\x00\x00\x04'))
# s.int32_member == 1
# s.int8_member == 4
# s.float_member == None
```

### Custom types
```python
from enum import IntEnum
from dataclasses import dataclass

from packer import *
from packer.protocols import TypeDescriptor

class FileTypes(IntEnum):
    UNK = 0
    TXT = 1
    BIN = 2

class _FileType(TypeDescriptor):
    _size: int = 1

    @classmethod
    def pack(cls, val: FileTypes) -> FileTypes:
        return val.to_bytes(1, "little")

    @classmethod
    def unpack(cls, data: bytes) -> FileTypes:
        return FileTypes(int.from_bytes(data[:cls._size], "little"))
    
FileType = _FileType | FileTypes # to get the typehint of FileTypes back

@packable
@dataclass
class File:
    file_type: Pack[FileType]
    file_data: Pack[AllData]

file = File(FileTypes.BIN, bytearray([3]*5))
file.pack() # bytearray(b'\x02\x03\x03\x03\x03\x03')

file.unpack(bytearray(b'\x01\x03\x03\x03\x03\x03hi!'))
# file.file_type == FileTypes.TXT
# file.data == b"\x03\x03\x03\x03\x03hi!"
```

### Packing a packable
**Nested packable attributes must have default values to ensure proper instantiation**

```python
@packable
@dataclass
class Header:
    data_type: Pack[int8] = None
    data_size: Pack[int32] = None

@packable
@dataclass
class Packet:
    header: Pack[Header]
    data: Pack[AllData]

packet = Packet(Header(1, 5), b"hello")
packet.pack() # bytearray(b"\x01\x05\x00\x00\x00hello")

packet.unpack(bytearray(b"\x04\x02\x00\x00\x00hi"))
# packet.header.data_type == 4
# packet.header.data_size == 2
# packet.data == hi
```