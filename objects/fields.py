from dataclasses import dataclass
from enum import auto, Enum

from objects.attributes import Attribute


class FieldFlags(Enum):
    ACC_PUBLIC = b'0001'
    ACC_PRIVATE = b'0002'
    ACC_PROTECTED = b'0004'
    ACC_STATIC = b'0008'
    ACC_FINAL = b'0010'
    ACC_VOLATILE = b'0040'
    ACC_TRANSIENT = b'0080'
    ACC_SYNTHETIC = b'1000'
    ACC_ENUM = b'4000'


@dataclass
class Field:
    access_flags: list[FieldFlags]
    name: int
    descriptor: int
    attributes_count: int
    attribute_info: list[Attribute]
