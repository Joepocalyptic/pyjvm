from dataclasses import dataclass
from enum import auto, Enum

from objects.attributes import Attribute


class MethodFlags(Enum):
    ACC_PUBLIC = b'0001'
    ACC_PRIVATE = b'0002'
    ACC_PROTECTED = b'0004'
    ACC_STATIC = b'0008'
    ACC_FINAL = b'0010'
    ACC_SYNCHRONIZED = b'0020'
    ACC_BRIDGE = b'0040'
    ACC_VARARGS = b'0080'
    ACC_NATIVE = b'0100'
    ACC_ABSTRACT = b'0400'
    ACC_STRICT = b'0800'
    ACC_SYNTHETIC = b'1000'


@dataclass
class Method:
    access_flags: list[MethodFlags]
    name_index: int
    descriptor_index: int
    attributes_count: int
    attribute_info: list[Attribute]