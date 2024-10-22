import dataclasses
from enum import IntEnum

from packer import *
from packer.protocols import (
    TypeDescriptor,
)


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
        return FileTypes(int.from_bytes(data[: cls._size], "little"))


FileType = _FileType | FileTypes  # to get the typehint back


def test_custom_type_packing() -> None:
    @packable
    @dataclasses.dataclass
    class File:
        file_type: Pack[FileType]
        file_data: Pack[AllData]

    assert File(FileTypes.TXT, b"hello!").pack() == b"\x01hello!"

    f = File(FileTypes.UNK, b"")

    f.unpack(File(FileTypes.BIN, bytearray([3] * 5)).pack())
    assert (
        f.file_type == FileTypes.BIN
        and len(f.file_data) == len(bytearray([3] * 5))
        and f.file_data == bytearray([3] * 5)
    )


if __name__ == "__main__":
    test_custom_type_packing()
