from dataclasses import dataclass, Field
from enum import Enum, auto

from objects.attributes import Attribute
from objects.constant_pool import ConstantPoolEntry
from objects.methods import Method


class ClassFlags(Enum):
    ACC_PUBLIC = auto()
    ACC_FINAL = auto()
    ACC_SUPER = auto()
    ACC_INTERFACE = auto()
    ACC_ABSTRACT = auto()
    ACC_SYNTHETIC = auto()
    ACC_ANNOTATION = auto()
    ACC_ENUM = auto()


@dataclass
class Class:
    minor_version: int
    major_version: int
    constant_pool_count: int
    constant_pool: list[ConstantPoolEntry]
    access_flags: list[ClassFlags]
    this_class: int
    super_class: int
    interfaces_count: int
    interfaces: list[int]
    fields_count: int
    fields: list[Field]
    methods_count: int
    methods: list[Method]
    attributes_count: int
    attribute_info: list[Attribute]
