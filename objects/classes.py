from dataclasses import dataclass, Field
from enum import Enum

from objects.attributes import Attribute
from objects.constant_pool import ConstantPoolEntry
from objects.methods import Method


class ClassFlags(Enum):
    ACC_PUBLIC = b'0001'
    ACC_SUPER = b'0020'
    ACC_FINAL = b'0010'
    ACC_INTERFACE = b'0200'
    ACC_ABSTRACT = b'0400'
    ACC_SYNTHETIC = b'1000'
    ACC_ANNOTATION = b'2000'
    ACC_ENUM = b'4000'


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
