from dataclasses import dataclass
from enum import Enum, auto


# --------------------------------------------------
# TYPE VERIFICATION
# --------------------------------------------------


class VerificationTypeInfo:
    pass


class TopVariableInfo(VerificationTypeInfo):
    pass


class IntegerVariableInfo(VerificationTypeInfo):
    pass


class FloatVariableInfo(VerificationTypeInfo):
    pass


class NullVariableInfo(VerificationTypeInfo):
    pass


class UninitializedThisVariableInfo(VerificationTypeInfo):
    pass


class ObjectVariableInfo(VerificationTypeInfo):
    cpool_index: int


class UninitializedVariableInfo(VerificationTypeInfo):
    offset: int


class LongVariableInfo(VerificationTypeInfo):
    pass


class DoubleVariableInfo(VerificationTypeInfo):
    pass


verification_type_union = {
    0: TopVariableInfo,
    1: IntegerVariableInfo,
    2: FloatVariableInfo,
    3: DoubleVariableInfo,
    4: LongVariableInfo,
    5: NullVariableInfo,
    6: UninitializedThisVariableInfo,
    7: ObjectVariableInfo,
    8: UninitializedVariableInfo
}


# --------------------------------------------------
# STACK MAP FRAMES
# --------------------------------------------------


class StackMapFrame:
    pass


@dataclass
class SameFrame(StackMapFrame):
    # Offset delta
    frame_type: int


@dataclass
class SameLocals1StackItemFrame(StackMapFrame):
    # Offset delta + 64
    frame_type: int
    stack: list[VerificationTypeInfo]


@dataclass
class SameLocals1StackItemFrameExtended(StackMapFrame):
    frame_type: int
    offset_delta: int
    stack: list[VerificationTypeInfo]


@dataclass
class ChopFrame(StackMapFrame):
    # k (missing locals) + 251
    frame_type: int
    offset_delta: int


@dataclass
class SameFrameExtended(StackMapFrame):
    frame_type: int
    offset_delta: int


@dataclass
class AppendFrame(StackMapFrame):
    frame_type: int
    offset_delta: int
    # [frame_type - 251]
    locals: list[VerificationTypeInfo]


@dataclass
class FullFrame(StackMapFrame):
    frame_type: int
    offset_delta: int
    number_of_locals: int
    locals: list[VerificationTypeInfo]
    number_of_stack_items: int
    stack: list[VerificationTypeInfo]


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


class Attribute:
    pass


@dataclass
class AttributeUnparsed:
    attribute_name_index: int
    attribute_length: int


@dataclass
class AttributeUnrecognized(Attribute):
    attribute_name_index: int
    attribute_length: int
    # bytes[attribute_length]
    info: bytes


@dataclass
class AttributeConstantValue(Attribute):
    constantvalue_index: int


@dataclass
class ExceptionHandler:
    start_pc: int
    end_pc: int
    handler_pc: int
    catch_type: int


@dataclass
class AttributeCode(Attribute):
    max_stack: int
    max_locals: int
    code_length: int
    code: bytes
    exception_table_length: int
    exception_table: list[ExceptionHandler]
    attributes_count: int
    attribute_info: list[Attribute]


@dataclass
class AttributeStackMapTable(Attribute):
    number_of_entries: int
    stack_map_frame: list[StackMapFrame]


@dataclass
class AttributeExceptions(Attribute):
    number_of_exceptions: int
    exception_index_table: list[int]


@dataclass
class AttributeExceptions(Attribute):
    number_of_exceptions: int
    exception_index_table: list[int]


@dataclass
class InnerClassEntry:
    inner_class_info_index: int
    outer_class_info_index: int
    inner_name_index: int
    inner_class_access_flags: int


@dataclass
class AttributeInnerClasses(Attribute):
    number_of_classes: int
    classes: list[InnerClassEntry]


@dataclass
class AttributeEnclosingMethod(Attribute):
    class_index: int
    method_index: int


@dataclass
class AttributeSynthetic(Attribute):
    pass


@dataclass
class AttributeSignature(Attribute):
    signature_index: int


@dataclass
class AttributeSourceFile(Attribute):
    sourcefile_index: int


@dataclass
class AttributeSourceDebugExtension(Attribute):
    debug_extension: bytes


@dataclass
class LineNumber:
    start_pc: int
    line_number: int


@dataclass
class AttributeLineNumberTable(Attribute):
    line_number_table_length: int
    line_number_table: list[LineNumber]


@dataclass
class LocalVariable:
    start_pc: int
    length: int
    name_index: int
    descriptor_index: int
    index: int


@dataclass
class AttributeLocalVariableTable(Attribute):
    local_variable_table_length: int
    local_variable_table: list[LocalVariable]


@dataclass
class LocalVariableType:
    start_pc: int
    length: int
    name_index: int
    signature_index: int
    index: int


@dataclass
class AttributeLocalVariableTypeTable(Attribute):
    local_variable_type_table_length: int
    local_variable_type_table: list[LocalVariableType]


@dataclass
class AttributeDeprecated(Attribute):
    pass


class ElementValue:
    pass


@dataclass
class ByteElementValue(ElementValue):
    const_value_index: int


@dataclass
class CharElementValue(ElementValue):
    const_value_index: int


@dataclass
class DoubleElementValue(ElementValue):
    const_value_index: int


@dataclass
class FloatElementValue(ElementValue):
    const_value_index: int


@dataclass
class IntElementValue(ElementValue):
    const_value_index: int


@dataclass
class LongElementValue(ElementValue):
    const_value_index: int


@dataclass
class ShortElementValue(ElementValue):
    const_value_index: int


@dataclass
class BooleanElementValue(ElementValue):
    const_value_index: int


@dataclass
class StringElementValue(ElementValue):
    const_value_index: int


@dataclass
class EnumValue:
    type_name_index: int
    const_name_index: int


@dataclass
class EnumElementValue(ElementValue):
    const_value_index: int


@dataclass
class ClassElementValue(ElementValue):
    class_info_index: int


@dataclass
class ArrayElementValue(ElementValue):
    num_values: int
    values: list[ElementValue]


@dataclass
class ElementValuePair:
    element_name_index: int
    element_value: ElementValue


@dataclass
class Annotation:
    type_index: int
    num_element_value_pairs: int
    element_value_pairs: list[ElementValuePair]


@dataclass
class AttributeRuntimeVisibleAnnotations(Attribute):
    num_annotations: int
    annotations: list[Annotation]


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
