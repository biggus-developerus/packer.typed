import dataclasses
import math
import struct

from packer import *


def test_float_packing() -> None:
    @packable
    @dataclasses.dataclass
    class FloatStruct:
        float_member: Pack[float32]

    f = FloatStruct(0.5)
    assert f.pack() == struct.pack("f", 0.5)

    f = FloatStruct(0.0)

    assert f.unpack(FloatStruct(69.42).pack())
    assert math.isclose(f.float_member, 69.42, rel_tol=1e-5, abs_tol=1e-5)


def test_simple_packing() -> None:
    @packable
    @dataclasses.dataclass
    class SimpleStruct:
        int32_member: Pack[int32] = 0
        int8_member: Pack[int8] = 0
        int8_member_optional: OptionalPack[int8] = 0

    assert SimpleStruct(1, 2, None).pack() == bytearray(b"\x01\x00\x00\x00\x02")
    assert SimpleStruct(1, 2, 2).pack() == bytearray(b"\x01\x00\x00\x00\x02\x02")

    s = SimpleStruct(0, 0, None)

    assert s.unpack(SimpleStruct(1, 2, None).pack())
    assert s.int32_member == 1 and s.int8_member == 2 and s.int8_member_optional == None

    s = SimpleStruct(0, 0, None)

    assert s.unpack(SimpleStruct(4, 4, 4).pack())
    assert s.int32_member == 4 and s.int8_member == 4 and s.int8_member_optional == 4


def test_all_data_packing() -> None:
    @packable
    @dataclasses.dataclass
    class AllDataStruct:
        int32_member: Pack[int32] = 0
        all_data_member: OptionalPack[AllData] = None

    s = AllDataStruct(4, b"hello!")
    assert s.pack() == bytearray(b"\x04\x00\x00\x00hello!")

    s = AllDataStruct(0, None)

    assert s.unpack(AllDataStruct(4, b"hello!").pack())
    assert s.int32_member == 4 and s.all_data_member == b"hello!"


def test_sized_packing() -> None:
    @packable
    @dataclasses.dataclass
    class SizedStruct:
        sized_member: Pack[Sized[5]]
        sized_member2: Pack[Sized[3]]

    assert SizedStruct(b"hello", b"hi!").pack() == b"hellohi!"
    s = SizedStruct(b"", b"")

    assert s.unpack(b"hellohi!")
    assert s.sized_member == b"hello"
    assert s.sized_member2 == b"hi!"


if __name__ == "__main__":
    test_float_packing()
    test_simple_packing()
    test_all_data_packing()
    test_sized_packing()
