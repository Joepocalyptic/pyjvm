from dataclasses import dataclass
from enum import auto, Enum

from objects.attributes import Attribute


class MethodFlags(Enum):
    ACC_PUBLIC = auto()
    ACC_PRIVATE = auto()
    ACC_PROTECTED = auto()
    ACC_STATIC = auto()
    ACC_FINAL = auto()
    ACC_SYNCHRONIZED = auto()
    ACC_BRIDGE = auto()
    ACC_VARARGS = auto()
    ACC_NATIVE = auto()
    ACC_ABSTRACT = auto()
    ACC_STRICT = auto()
    ACC_SYNTHETIC = auto()


@dataclass
class Method:
    access_flags: list[MethodFlags]
    name_index: int
    descriptor_index: int
    attributes_count: int
    attribute_info: list[Attribute]