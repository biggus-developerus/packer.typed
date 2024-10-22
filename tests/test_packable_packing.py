from dataclasses import (
    dataclass,
)

from packer import *


def test_packable_packing() -> None:
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
    assert (
        packet.pack() == b"\x01\x05\x00\x00\x00hello"
        and len(packet.data) == packet.header.data_size
    )

    assert packet.unpack(b"\x05\x02\x00\x00\x00hi")
    assert (
        packet.header.data_type == 5
        and packet.header.data_size == 2
        and len(packet.data) == packet.header.data_size
    )


if __name__ == "__main__":
    test_packable_packing()
