from dataclasses import dataclass
from enum import Enum, auto


# --------------------------------------------------
# TYPE VERIFICATION
# --------------------------------------------------
from opcodes import Opcode


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


@dataclass
class ObjectVariableInfo(VerificationTypeInfo):
    cpool_index: int


@dataclass
class UninitializedVariableInfo(VerificationTypeInfo):
    offset: int


class LongVariableInfo(VerificationTypeInfo):
    pass


class DoubleVariableInfo(VerificationTypeInfo):
    pass


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
    parsed_code: list[Opcode]
    exception_table_length: int
    exception_table: list[ExceptionHandler]
    attributes_count: int
    attribute_info: list[Attribute]


@dataclass
class AttributeStackMapTable(Attribute):
    number_of_entries: int
    entries: list[StackMapFrame]


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
class EnumElementValue:
    type_name_index: int
    const_name_index: int


@dataclass
class ClassElementValue(ElementValue):
    class_info_index: int


@dataclass
class ElementValuePair:
    element_name_index: int
    element_value: ElementValue


@dataclass
class Annotation(ElementValue):
    type_index: int
    num_element_value_pairs: int
    element_value_pairs: list[ElementValuePair]


@dataclass
class ArrayElementValue(ElementValue):
    num_values: int
    values: list[ElementValue]


@dataclass
class AttributeRuntimeVisibleAnnotations(Attribute):
    num_annotations: int
    annotations: list[Annotation]


@dataclass
class AttributeRuntimeInvisibleAnnotations(Attribute):
    num_annotations: int
    annotations: list[Annotation]


@dataclass
class ParameterAnnotations:
    num_annotations: int
    annotations: list[Annotation]


@dataclass
class AttributeRuntimeVisibleParameterAnnotations(Attribute):
    num_parameters: int
    parameter_annotations: list[ParameterAnnotations]


@dataclass
class AttributeRuntimeInvisibleParameterAnnotations(Attribute):
    num_parameters: int
    parameter_annotations: list[ParameterAnnotations]


class TargetInfo:
    pass


@dataclass
class TypeParameterTarget(TargetInfo):
    type_parameter_index: int


@dataclass
class SupertypeTarget(TargetInfo):
    supertype_index: int


@dataclass
class TypeParameterBoundTarget(TargetInfo):
    type_parameter_index: int
    bound_index: int


@dataclass
class EmptyTarget(TargetInfo):
    pass


@dataclass
class FormalParameterTarget(TargetInfo):
    formal_parameter_index: int


@dataclass
class ThrowsTarget(TargetInfo):
    throws_type_index: int


@dataclass
class LocalvarInfo:
    start_pc: int
    length: int
    index: int


@dataclass
class LocalvarTarget(TargetInfo):
    table_length: int
    table: list[LocalvarInfo]


@dataclass
class CatchTarget(TargetInfo):
    exception_table_index: int


@dataclass
class OffsetTarget(TargetInfo):
    offset: int


@dataclass
class TypeArgumentTarget(TargetInfo):
    offset: int
    type_argument_index: int


@dataclass
class PathStep:
    type_path_kind: int
    type_argument_index: int


@dataclass
class TypePath:
    path_length: int
    path: list[PathStep]


@dataclass
class TypeAnnotation:
    target_type: str
    target_info: TargetInfo
    target_path: TypePath
    type_index: int
    num_element_value_pairs: int
    element_value_pairs: list[ElementValuePair]


@dataclass
class AttributeRuntimeVisibleTypeAnnotations(Attribute):
    num_annotations: int
    annotations: list[TypeAnnotation]


@dataclass
class AttributeRuntimeInvisibleTypeAnnotations(Attribute):
    num_annotations: int
    annotations: list[TypeAnnotation]


@dataclass
class AttributeAnnotationDefault(Attribute):
    default_value: ElementValue


@dataclass
class BootstrapMethod:
    bootstrap_method_ref: int
    num_bootstrap_arguments: int
    bootstrap_arguments: list[int]


@dataclass
class AttributeBootstrapMethods(Attribute):
    num_bootstrap_methods: int
    bootstrap_methods: list[BootstrapMethod]


class MethodParameterFlags(Enum):
    ACC_FINAL = auto()
    ACC_SYNTHETIC = auto()
    ACC_MANDATED = auto()


@dataclass
class MethodParameter:
    name_index: int
    access_flags: list[MethodParameterFlags]


@dataclass
class AttributeMethodParameters(Attribute):
    num_bootstrap_methods: int
    bootstrap_methods: list[MethodParameter]


# --------------------------------------------------
# FIELDS & METHODS
# --------------------------------------------------


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
