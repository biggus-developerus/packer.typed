from dataclasses import (
    dataclass,
)

from packer import (
    OptionalPack,
    Pack,
    TypeDescriptor,
    packable,
)


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
    test1: Pack[LengthPrefixedStr] = "test"
    test2: OptionalPack[LengthPrefixedStr] = "test2"


def test_custom_packing() -> bool:
    val = CustomTypesStruct().pack()
    assert val == bytearray(b"\x04\x00test\x05\x00test2")

    val = CustomTypesStruct("test", None).pack()
    assert val == bytearray(b"\x04\x00test")


if __name__ == "__main__":
    test_custom_packing()
