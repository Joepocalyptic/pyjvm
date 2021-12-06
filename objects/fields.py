from dataclasses import dataclass
from enum import auto, Enum

from objects.attributes import Attribute


class FieldFlags(Enum):
    ACC_PUBLIC = auto()
    ACC_PRIVATE = auto()
    ACC_PROTECTED = auto()
    ACC_STATIC = auto()
    ACC_FINAL = auto()
    ACC_VOLATILE = auto()
    ACC_TRANSIENT = auto()
    ACC_SYNTHETIC = auto()
    ACC_ENUM = auto()


@dataclass
class Field:
    access_flags: list[FieldFlags]
    name_index: int
    descriptor_index: int
    attributes_count: int
    attribute_info: list[Attribute]
