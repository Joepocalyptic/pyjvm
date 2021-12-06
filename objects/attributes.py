from dataclasses import dataclass
from enum import Enum, auto

from objects.stack_map_frames import StackMapFrame
from opcodes import ParsedOpcode


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
    code: dict[int, ParsedOpcode]
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
class EnumElementValue(ElementValue):
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
