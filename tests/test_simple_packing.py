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
class SimpleStruct:
    id: Pack[Int32] = 0
    val: OptionalPack[Float] = None


def test_simple_packing() -> bool:
    t = SimpleStruct()
    t.unpack(bytearray([1, 0, 0, 0]) + struct.pack("f", 1.0))

    assert t.id == 1 and t.val and math.isclose(t.val, 1.0, rel_tol=4e-9)

    t = SimpleStruct()
    t.unpack(bytearray([1, 0, 0, 0] * 1))

    assert t.id == 1 and t.val == None
    assert t.pack() == bytearray([1, 0, 0, 0])


if __name__ == "__main__":
    test_simple_packing()
