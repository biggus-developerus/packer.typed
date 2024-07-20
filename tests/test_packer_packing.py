import math
import struct
from dataclasses import (
    dataclass,
)

from packer import (
    Float,
    Int32,
    OptionalPack,
    Pack,
    packable,
)


@packable
@dataclass
class TestPack:
    id: Pack[Int32] = 69


@packable
@dataclass
class TestPack2:
    test: Pack[Float] = 6.9


@packable
@dataclass
class PackAPackerXd:
    test1: Pack[TestPack]
    test2: Pack[TestPack2]


def test_packer_packing() -> bool:
    t = PackAPackerXd(TestPack(1), TestPack2(1.0))
    data = t.pack()

    assert len(data) == 8 and data == bytearray(b"\x01\x00\x00\x00\x00\x00\x80?")


if __name__ == "__main__":
    test_packer_packing()
