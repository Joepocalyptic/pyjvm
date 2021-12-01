from dataclasses import dataclass
from enum import Enum, auto


# --------------------------------------------------
# CONSTANT POOL
# --------------------------------------------------


class ConstantPoolEntry:
    pass


@dataclass
class ConstantClassInfo(ConstantPoolEntry):
    # ConstantUtf8Info
    name_index: int


@dataclass
class ConstantFieldrefInfo(ConstantPoolEntry):
    # ConstantClassInfo
    class_index: int
    # ConstantNameAndTypeInfo
    name_and_type_index: int


@dataclass
class ConstantMethodrefInfo(ConstantPoolEntry):
    # ConstantClassInfo
    class_index: int
    # ConstantNameAndTypeInfo
    name_and_type_index: int


@dataclass
class ConstantInterfaceMethodrefInfo(ConstantPoolEntry):
    # ConstantClassInfo
    class_index: int
    # ConstantNameAndTypeInfo
    name_and_type_index: int


@dataclass
class ConstantStringInfo(ConstantPoolEntry):
    # ConstantUtf8Info
    string_index: int


@dataclass
class ConstantIntegerInfo(ConstantPoolEntry):
    # Bytes
    bytes: bytes


@dataclass
class ConstantFloatInfo(ConstantPoolEntry):
    bytes: bytes


@dataclass
class ConstantLongInfo(ConstantPoolEntry):
    high_bytes: bytes
    low_bytes: bytes


@dataclass
class ConstantDoubleInfo(ConstantPoolEntry):
    high_bytes: bytes
    low_bytes: bytes


@dataclass
class ConstantNameAndTypeInfo(ConstantPoolEntry):
    # ConstantUtf8Info
    name_index: int
    # ConstantUtf8Info
    descriptor_index: int


@dataclass
class ConstantUtf8Info(ConstantPoolEntry):
    length: int
    # bytearray[length]
    bytes: bytes


@dataclass
class ConstantMethodHandleInfo(ConstantPoolEntry):
    reference_kind: int
    # ConstantFieldrefInfo || ConstantMethodrefInfo || ConstantInterfaceMethodrefInfo
    reference_index: int


@dataclass
class ConstantMethodTypeInfo(ConstantPoolEntry):
    # ConstantUtf8Info
    descriptor_index: int


@dataclass
class ConstantInvokeDynamicInfo(ConstantPoolEntry):
    # bootstrap_methods index
    bootstrap_method_attr_index: int
    # ConstantNameAndTypeInfo
    name_and_type_index: int


# --------------------------------------------------
# ATTRIBUTES
# --------------------------------------------------


@dataclass
class Attribute:
    attribute_name_index: int
    attribute_length: int
    # bytes[attribute_length]
    info: bytes


# --------------------------------------------------
# FIELDS & METHODS
# --------------------------------------------------


@dataclass
class Field:
    access_flags: str
    name_index: int
    descriptor_index: int
    attributes_count: int
    attribute_info: list[Attribute]


@dataclass
class Method:
    access_flags: str
    name_index: int
    descriptor_index: int
    attributes_count: int
    attribute_info: list[Attribute]


# --------------------------------------------------
# CLASS
# --------------------------------------------------


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
    constant_pool_size: int
    constant_pool: list[ConstantPoolEntry]
    access_flags: list[ClassFlags]
    this_class: int
    super_class: int
    interfaces_count: int
    interfaces: list[ConstantClassInfo]
    fields_count: int
