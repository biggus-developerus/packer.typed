import math
import struct
from dataclasses import (
    dataclass,
)

from packer import (
    Pack,
    SizedData,
    packable,
)


@packable
@dataclass
class SizedDataStruct:
    sized_data: Pack[SizedData[10]] = None
    sized_data2: Pack[SizedData[50]] = None


def test_sized_packing() -> bool:
    t = SizedDataStruct()
    t.sized_data = bytearray(b"h" * 5 + b"i" * 5)
    t.sized_data2 = bytearray(50)

    assert len(t.pack()) == 60 and t.pack() == bytearray(
        b"hhhhhiiiii\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    )
    assert t.unpack(bytearray(b"x" * 5 + b"d" * 5) + bytearray(50)) == 60
    assert t.sized_data == bytearray(b"x" * 5 + b"d" * 5)
    assert t.sized_data2 == bytearray(50)


if __name__ == "__main__":
    test_sized_packing()
