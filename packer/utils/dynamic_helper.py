__all__ = ("create_pack_pair",)

from typing import (
    TYPE_CHECKING,
    Callable,
    Type,
    TypeVar,
)

if TYPE_CHECKING:
    from packer.packer import PackData

from packer.pack_types import *

TEMPLATE_PACK_METHOD = """
def {}(self):
    data = bytearray()
    {}
    return data
"""

TEMPLATE_UNPACK_METHOD = """
def {}(self, data):
    {}
"""

T = TypeVar("T")


def create_pack_pair(
    cls: Type[T],
    packing_data: list["PackData"],
) -> tuple[Callable[[], bytearray], Callable[[bytearray], None]]:
    pack_method_body = []
    unpack_method_body = [""]  # for the size check

    total_min_size = 0

    # TODO: Make this eyesore not an eyesore..?
    for pack in packing_data:
        is_extended = getattr(pack.type_descriptor, "__is_extended_packable__", False)

        if pack.optional:
            pack_method_body.append(f"if not self.{pack.attr_name}: return data")
            unpack_method_body.append(
                f"if len(data) < {pack.offset + pack.type_descriptor._size}: return True"  # return true cuz it's optional
            )
        else:
            total_min_size += pack.type_descriptor._size

        pack_method_body.append(
            f"data += {pack.type_descriptor.__name__}.pack(self.{pack.attr_name})"
        )

        if pack.type_descriptor._size > 0:
            if is_extended:
                unpack_method_body.append(
                    f"self.{pack.attr_name} = {pack.type_descriptor.__name__}()"
                )
                unpack_method_body.append(
                    f"self.{pack.attr_name}.unpack(data[{pack.offset}:{pack.offset + pack.type_descriptor._size}])"
                )
            else:
                unpack_method_body.append(
                    f"self.{pack.attr_name} = {pack.type_descriptor.__name__}.unpack(data[{pack.offset}:{pack.offset + pack.type_descriptor._size}])"
                )
        else:
            if is_extended:
                unpack_method_body.append(
                    f"self.{pack.attr_name} = {pack.type_descriptor.__name__}()"
                )
                unpack_method_body.append(
                    f"self.{pack.attr_name}.unpack(data[{pack.offset}:{pack.offset + pack.type_descriptor._size}])"
                )
            else:
                unpack_method_body.append(
                    f"self.{pack.attr_name} = {pack.type_descriptor.__name__}.unpack(data[{pack.offset}:len(data)])"
                )

        globals()[pack.type_descriptor.__name__] = pack.type_descriptor

    unpack_method_body[0] = f"if len(data) < {total_min_size}: return False"
    unpack_method_body.append(f"return True")

    pack_func_name, pack_func_code = f"__{cls.__name__}_pack__", "\n    ".join(pack_method_body)
    unpack_func_name, unpack_func_code = f"__{cls.__name__}_unpack__", "\n    ".join(
        unpack_method_body
    )

    # TODO: Find a better way of doing this.. sketchy ash fr on skibidi sigma ohio rizz
    exec(TEMPLATE_PACK_METHOD.format(pack_func_name, pack_func_code), globals())
    exec(TEMPLATE_UNPACK_METHOD.format(unpack_func_name, unpack_func_code), globals())

    # print(TEMPLATE_PACK_METHOD.format(pack_func_name, pack_func_code))
    # print(TEMPLATE_UNPACK_METHOD.format(unpack_func_name, unpack_func_code))

    return (
        lambda self, cb=globals()[pack_func_name]: cb(self),
        lambda self, data, cb=globals()[unpack_func_name]: cb(self, data),
    )
