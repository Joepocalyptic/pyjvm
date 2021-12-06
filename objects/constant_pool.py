from dataclasses import dataclass


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