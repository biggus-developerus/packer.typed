import math
import struct
import packer

from dataclasses import (
    dataclass,
)

from packer import (
    OptionalPack,
    Pack,
    packable,
    int8,
    int32,
    float
)


@packable
@dataclass
class SimpleStruct:
    int32_member: Pack[int32] = 0
    int8_member: Pack[int8] = 0
    int8_member_optional: OptionalPack[int8] = 0


@packable
@dataclass
class FloatStruct:
    float_member: Pack[packer.pack_types.Float]


def test_float_packing() -> None:
    f = FloatStruct(0.5)
    assert f.pack() == struct.pack("f", 0.5)

    f = FloatStruct(0.0)
    f.unpack(FloatStruct(69.42).pack())
    assert math.isclose(f.float_member, 69.42, rel_tol=1e-5, abs_tol=1e-5)


def test_simple_packing() -> None:
    assert SimpleStruct(1, 2, None).pack() == bytearray(b"\x01\x00\x00\x00\x02\x00")
    assert SimpleStruct(1, 2, 2).pack() == bytearray(b"\x01\x00\x00\x00\x02\x00\x02\x00")

    s = SimpleStruct(0, 0, None)
    s.unpack(SimpleStruct(1, 2, None).pack())

    assert s.int32_member == 1 and s.int8_member == 2 and s.int8_member_optional == None

    s = SimpleStruct(0, 0, None)
    s.unpack(SimpleStruct(4, 4, 4).pack())

    assert s.int32_member == 4 and s.int8_member == 4 and s.int8_member_optional == 4


if __name__ == "__main__":
    test_float_packing()
    test_simple_packing()
