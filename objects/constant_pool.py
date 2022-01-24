from dataclasses import dataclass


class ConstantPoolEntry:
    tag: int

class PConstantPoolEntry:
    pass


@dataclass
class ConstantNameAndTypeInfo(ConstantPoolEntry):
    tag = 12
    # ConstantUtf8Info
    name_index: int
    # ConstantUtf8Info
    descriptor_index: int


@dataclass
class PConstantNameAndTypeInfo(PConstantPoolEntry):
    name: str
    descriptor: str


@dataclass
class ConstantClassInfo(ConstantPoolEntry):
    tag = 7
    # ConstantUtf8Info
    name_index: int


@dataclass
class PConstantClassInfo(PConstantPoolEntry):
    name: str


@dataclass
class ConstantFieldrefInfo(ConstantPoolEntry):
    tag = 9
    # ConstantClassInfo
    class_index: int
    # ConstantNameAndTypeInfo
    name_and_type_index: int


@dataclass
class PConstantFieldrefInfo(PConstantPoolEntry):
    clazz: PConstantClassInfo
    name_and_type: PConstantNameAndTypeInfo


@dataclass
class ConstantMethodrefInfo(ConstantPoolEntry):
    tag = 10
    # ConstantClassInfo
    class_index: int
    # ConstantNameAndTypeInfo
    name_and_type_index: int


@dataclass
class PConstantMethodrefInfo(PConstantPoolEntry):
    clazz: PConstantClassInfo
    name_and_type: PConstantNameAndTypeInfo


@dataclass
class ConstantInterfaceMethodrefInfo(ConstantPoolEntry):
    tag = 11
    # ConstantClassInfo
    class_index: int
    # ConstantNameAndTypeInfo
    name_and_type_index: int


@dataclass
class PConstantInterfaceMethodrefInfo(PConstantPoolEntry):
    clazz: PConstantClassInfo
    name_and_type: PConstantNameAndTypeInfo


@dataclass
class ConstantStringInfo(ConstantPoolEntry):
    tag = 8
    # ConstantUtf8Info
    string_index: int


@dataclass
class PConstantStringInfo(PConstantPoolEntry):
    string: str


@dataclass
class ConstantIntegerInfo(ConstantPoolEntry):
    tag = 3
    bytes: bytes


@dataclass
class PConstantIntegerInfo(PConstantPoolEntry):
    value: int


@dataclass
class ConstantFloatInfo(ConstantPoolEntry):
    tag = 4
    bytes: bytes


@dataclass
class PConstantFloatInfo(PConstantPoolEntry):
    value: float


@dataclass
class ConstantLongInfo(ConstantPoolEntry):
    tag = 5
    high_bytes: bytes
    low_bytes: bytes


@dataclass
class PConstantLongInfo(PConstantPoolEntry):
    value: int


@dataclass
class ConstantDoubleInfo(ConstantPoolEntry):
    tag = 6
    high_bytes: bytes
    low_bytes: bytes


@dataclass
class PConstantDoubleInfo(PConstantPoolEntry):
    value: float


@dataclass
class ConstantUtf8Info(ConstantPoolEntry):
    tag = 1
    length: int
    # bytearray[length]
    bytes: bytes


@dataclass
class ConstantMethodHandleInfo(ConstantPoolEntry):
    tag = 15
    reference_kind: int
    # ConstantFieldrefInfo || ConstantMethodrefInfo || ConstantInterfaceMethodrefInfo
    reference_index: int


@dataclass
class PConstantMethodHandleInfo(PConstantPoolEntry):
    reference_kind: int
    reference: PConstantPoolEntry


@dataclass
class ConstantMethodTypeInfo(ConstantPoolEntry):
    tag = 16
    # ConstantUtf8Info
    descriptor_index: int


@dataclass
class PConstantMethodTypeInfo(PConstantPoolEntry):
    descriptor: str


@dataclass
class ConstantInvokeDynamicInfo(ConstantPoolEntry):
    tag = 18
    # bootstrap_methods index
    bootstrap_method_attr_index: int
    # ConstantNameAndTypeInfo
    name_and_type_index: int


@dataclass
class PConstantInvokeDynamicInfo(PConstantPoolEntry):
    # bootstrap_methods index
    bootstrap_method_attr_index: int
    # ConstantNameAndTypeInfo
    name_and_type: PConstantNameAndTypeInfo