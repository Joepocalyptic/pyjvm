from binascii import hexlify

from objects.attributes import *
from objects.attributes_ext import AnnotationElementValue
from objects.classes import *
from objects.constant_pool import *
from objects.errors import VerifyError
from objects.fields import *
from objects.methods import *
from objects.type_verification import *
from objects.stack_map_frames import *

from opcodes import opcodes, ParsedOpcode


# --------------------------------------------------
# CLASS STRUCTURE
# --------------------------------------------------


def parse_class(filename) -> Class:
    file = open(filename, "rb")

    # All valid class files must start with 0xCAFEBABE
    if hex_(file.read(4)) != b"cafebabe":
        file.close()
        raise VerifyError(f"Failed to parse class: invalid magic number; likely not a class file")

    minor_version = uint(file.read(2))
    major_version = uint(file.read(2))

    # Currently only targeting class spec 52.0 (Java SE 8)
    if f"{major_version}.{minor_version}" != "52.0":
        file.close()
        raise VerifyError(f"Failed to parse class: unsupported major/minor version {major_version}.{minor_version}")

    # Parse constant pool
    constant_pool_count = uint(file.read(2))
    constant_pool = list()

    # noinspection PyTypeChecker
    # Bump to 1-indexed list
    constant_pool.append(None)

    # Iterate through constant pool
    pool_count = constant_pool_count-1
    for _ in range(pool_count):
        constant_type = uint(file.read(1))
        entry = parse_constant_pool_entry(file, constant_type)
        constant_pool.append(entry)

    # Decode access flag mask
    access_flags = parse_class_flags(file)

    this_class = uint(file.read(2))
    super_class = uint(file.read(2))

    # Parse superinterfaces
    interfaces_count = uint(file.read(2))
    interfaces = list()

    # Iterate through superinterfaces
    for _ in range(interfaces_count):
        interfaces.append(uint(file.read(2)))

    # Parse fields
    fields_count = uint(file.read(2))
    fields = list()

    # Iterate through fields
    for _ in range(fields_count):
        fields.append(parse_field_method(file, False, constant_pool))

    # Parse methods
    methods_count = uint(file.read(2))
    methods = list()

    # Iterate through methods
    for _ in range(methods_count):
        methods.append(parse_field_method(file, True, constant_pool))

    # Parse class attributes
    attributes_count = uint(file.read(2))
    attribute_info = list()

    # Iterate through attributes
    for _ in range(attributes_count):
        attribute_name_index = uint(file.read(2))
        attribute_length = uint(file.read(4))

        attribute_info.append(parse_attribute(AttributeUnparsed(
            attribute_name_index,
            attribute_length
        ), file, constant_pool))

    # Parsing complete; ready for validation
    # TODO: Class validation

    clazz = Class(
        minor_version,
        major_version,
        constant_pool_count,
        constant_pool,
        access_flags,
        this_class,
        super_class,
        interfaces_count,
        interfaces,
        fields_count,
        fields,
        methods_count,
        methods,
        attributes_count,
        attribute_info
    )

    file.close()
    return clazz


def parse_constant_pool_entry(file, constant_type):
    match constant_type:
        case 1:
            length = uint(file.read(2))
            return ConstantUtf8Info(length, file.read(length))
        case 3:
            return ConstantIntegerInfo(file.read(4))
        case 4:
            return ConstantFloatInfo(file.read(4))
        case 5:
            return ConstantLongInfo(file.read(4), file.read(4))
        case 6:
            return ConstantLongInfo(file.read(4), file.read(4))
        case 7:
            return ConstantClassInfo(uint(file.read(2)))
        case 8:
            return ConstantStringInfo(uint(file.read(2)))
        case 9:
            return ConstantFieldrefInfo(
                uint(file.read(2)),
                uint(file.read(2))
            )
        case 10:
            return ConstantMethodrefInfo(
                uint(file.read(2)),
                uint(file.read(2))
            )
        case 11:
            return ConstantInterfaceMethodrefInfo(
                uint(file.read(2)),
                uint(file.read(2))
            )
        case 12:
            return ConstantNameAndTypeInfo(
                uint(file.read(2)),
                uint(file.read(2))
            )
        case 15:
            return ConstantMethodHandleInfo(
                uint(file.read(1)),
                uint(file.read(2))
            )
        case 16:
            return ConstantMethodTypeInfo(uint(file.read(2)))
        case 18:
            return ConstantInvokeDynamicInfo(
                uint(file.read(2)),
                uint(file.read(2))
            )
        case _:
            raise VerifyError(f"Failed to parse class: invalid constant type {constant_type}")


# --------------------------------------------------
# ATTRIBUTES
# --------------------------------------------------


def parse_attribute(attribute, file, constant_pool):
    attribute_name = constant_pool[attribute.attribute_name_index].bytes.decode("utf-8")
    match attribute_name:
        case "ConstantValue":
            return AttributeConstantValue(uint(file.read(2)))

        case "Code":
            max_stack = uint(file.read(2))
            max_locals = uint(file.read(2))
            code_length = uint(file.read(4))

            code = parse_bytecode(file.read(code_length))

            exception_table_length = uint(file.read(2))
            exception_table = list()

            for _ in range(exception_table_length):
                exception_table.append(ExceptionHandler(
                    uint(file.read(2)),
                    uint(file.read(2)),
                    uint(file.read(2)),
                    uint(file.read(2))
                ))

            attributes_count = uint(file.read(2))
            attribute_info = list()

            # Iterate through nested attributes
            for _ in range(attributes_count):
                attribute_name_index = uint(file.read(2))
                attribute_length = uint(file.read(4))

                attribute_info.append(parse_attribute(AttributeUnparsed(
                    attribute_name_index,
                    attribute_length
                ), file, constant_pool))

            return AttributeCode(
                max_stack,
                max_locals,
                code_length,
                code,
                exception_table_length,
                exception_table,
                attributes_count,
                attribute_info
            )

        case "StackMapTable":
            number_of_entries = uint(file.read(2))
            entries = list()

            for _ in range(number_of_entries):
                tag = uint(file.read(1))
                match tag:
                    # SameFrame
                    case tag if tag in range(0, 64):
                        entries.append(SameFrame(tag))

                    # SameLocals1StackItemFrame
                    case tag if tag in range(64, 128):
                        stack = list()
                        stack.append(parse_verification_type_info(file))

                        entries.append(SameLocals1StackItemFrame(tag, stack))

                    # SameLocals1StackItemFrameExtended
                    case tag if tag == 247:
                        offset_delta = uint(file.read(2))

                        stack = list()
                        stack.append(parse_verification_type_info(file))

                        entries.append(SameLocals1StackItemFrameExtended(tag, offset_delta, stack))

                    # ChopFrame
                    case tag if tag in range(248, 251):
                        offset_delta = uint(file.read(2))

                        entries.append(ChopFrame(tag, offset_delta))

                    # SameFrameExtended
                    case tag if tag == 251:
                        offset_delta = uint(file.read(2))

                        entries.append(SameFrameExtended(tag, offset_delta))

                    # AppendFrame
                    case tag if tag in range(252, 255):
                        offset_delta = uint(file.read(2))

                        localz = list()
                        for _ in range(tag-251):
                            # TODO: Double and long might need special treatment
                            localz.append(parse_verification_type_info(file))

                        entries.append(AppendFrame(tag, offset_delta, localz))

                    # FullFrame
                    case tag if tag == 255:
                        offset_delta = uint(file.read(2))

                        number_of_locals = uint(file.read(2))
                        localz = list()
                        for _ in range(number_of_locals):
                            localz.append(parse_verification_type_info(file))

                        number_of_stack_items = uint(file.read(2))
                        stack = list()
                        for _ in range(number_of_stack_items):
                            stack.append(parse_verification_type_info(file))

                        entries.append(FullFrame(
                            tag,
                            offset_delta,
                            number_of_locals,
                            localz,
                            number_of_stack_items,
                            stack
                        ))

                    # Not in spec
                    case _:
                        raise VerifyError(f"Failed to parse class: invalid StackMapTable union tag {tag}")

            return AttributeStackMapTable(number_of_entries, entries)

        case "Exceptions":
            number_of_exceptions = uint(file.read(2))
            exception_index_table = list()

            for _ in range(number_of_exceptions):
                exception_index_table.append(uint(file.read(2)))

            return AttributeExceptions(number_of_exceptions, exception_index_table)

        case "InnerClasses":
            number_of_classes = uint(file.read(2))
            classes = list()

            for _ in range(number_of_classes):
                classes.append(InnerClassEntry(
                    uint(file.read(2)),
                    uint(file.read(2)),
                    uint(file.read(2)),
                    uint(file.read(2))
                ))

            return AttributeInnerClasses(number_of_classes, classes)

        case "EnclosingMethod":
            return AttributeEnclosingMethod(
                uint(file.read(2)),
                uint(file.read(2))
            )

        case "Synthetic":
            return AttributeSynthetic()

        case "Signature":
            # TODO: Parse signatures
            return AttributeSignature(
                uint(file.read(2))
            )

        case "SourceFile":
            return AttributeSourceFile(
                uint(file.read(2))
            )

        case "SourceDebugExtension":
            return AttributeSourceDebugExtension(file.read(attribute.attribute_length))

        case "LineNumberTable":
            line_number_table_length = uint(file.read(2))
            line_number_table = list()

            for _ in range(line_number_table_length):
                line_number_table.append(LineNumber(
                    uint(file.read(2)),
                    uint(file.read(2))
                ))

            return AttributeLineNumberTable(line_number_table_length, line_number_table)

        case "LocalVariableTable":
            local_variable_table_length = uint(file.read(2))
            local_variable_table = list()

            for _ in range(local_variable_table_length):
                local_variable_table.append(LocalVariable(
                    uint(file.read(2)),
                    uint(file.read(2)),
                    uint(file.read(2)),
                    uint(file.read(2)),
                    uint(file.read(2))
                ))

            return AttributeLocalVariableTable(local_variable_table_length, local_variable_table)

        case "LocalVariableTypeTable":
            local_variable_type_table_length = uint(file.read(2))
            local_variable_type_table = list()

            for _ in range(local_variable_type_table_length):
                local_variable_type_table.append(LocalVariableType(
                    uint(file.read(2)),
                    uint(file.read(2)),
                    uint(file.read(2)),
                    uint(file.read(2)),
                    uint(file.read(2))
                ))

            return AttributeLocalVariableTypeTable(local_variable_type_table_length, local_variable_type_table)

        case "Deprecated":
            return AttributeDeprecated()

        case "RuntimeVisibleAnnotations":
            num_annotations = uint(file.read(2))
            annotations = list()

            for _ in range(num_annotations):
                annotations.append(parse_annotation(file))

            return AttributeRuntimeVisibleAnnotations(num_annotations, annotations)

        case "RuntimeInvisibleAnnotations":
            num_annotations = uint(file.read(2))
            annotations = list()

            for _ in range(num_annotations):
                annotations.append(parse_annotation(file))

            return AttributeRuntimeInvisibleAnnotations(num_annotations, annotations)

        case "RuntimeVisibleParameterAnnotations":
            num_parameters = uint(file.read(2))
            parameter_annotations = list()

            for _ in range(num_parameters):
                num_annotations = uint(file.read(2))
                annotations = list()

                for _ in range(num_annotations):
                    annotations.append(parse_annotation(file))

                parameter_annotations.append(ParameterAnnotations(num_annotations, annotations))

            return AttributeRuntimeVisibleParameterAnnotations(num_parameters, parameter_annotations)

        case "RuntimeInvisibleParameterAnnotations":
            num_parameters = uint(file.read(2))
            parameter_annotations = list()

            for _ in range(num_parameters):
                num_annotations = uint(file.read(2))
                annotations = list()

                for _ in range(num_annotations):
                    annotations.append(parse_annotation(file))

                parameter_annotations.append(ParameterAnnotations(num_annotations, annotations))

            return AttributeRuntimeInvisibleParameterAnnotations(num_parameters, parameter_annotations)

        case "RuntimeVisibleTypeAnnotations":
            num_annotations = uint(file.read(2))
            annotations = list()

            for _ in range(num_annotations):
                annotations.append(parse_typeannotation(file))

            return AttributeRuntimeVisibleTypeAnnotations(num_annotations, annotations)

        case "RuntimeInvisibleTypeAnnotations":
            num_annotations = uint(file.read(2))
            annotations = list()

            for _ in range(num_annotations):
                annotations.append(parse_typeannotation(file))

            return AttributeRuntimeInvisibleTypeAnnotations(num_annotations, annotations)

        case "AnnotationDefault":
            return AttributeAnnotationDefault(parse_element_value(file))

        case "BootstrapMethods":
            num_bootstrap_methods = uint(file.read(2))
            bootstrap_methods = list()

            for _ in range(num_bootstrap_methods):
                bootstrap_method_ref = uint(file.read(2))
                num_bootstrap_arguments = uint(file.read(2))
                bootstrap_arguments = list()

                for _ in range(num_bootstrap_arguments):
                    bootstrap_arguments.append(uint(file.read(2)))

                bootstrap_methods.append(BootstrapMethod(
                    bootstrap_method_ref,
                    num_bootstrap_arguments,
                    bootstrap_arguments
                ))

            return AttributeBootstrapMethods(num_bootstrap_methods, bootstrap_methods)

        case "MethodParameters":
            parameters_count = uint(file.read(1))
            parameters = list()

            for _ in range(parameters_count):
                parameters.append(MethodParameter(
                    uint(file.read(2)),
                    parse_method_parameter_flags(file)
                ))

            return AttributeMethodParameters(parameters_count, parameters)

        case _:
            # Not in spec; silently ignore and return ambiguous object
            return AttributeUnrecognized(
                attribute.attribute_name_index,
                attribute.attribute_length,
                file.read(attribute.attribute_length)
            )


def parse_bytecode(code):
    operations = dict[int, ParsedOpcode]()

    i = 0
    while i < len(code):
        try:
            opcode = opcodes[code[i]]
        except IndexError:
            raise VerifyError(f"Failed to parse class: unknown opcode {code[i]}")

        match code[i]:
            # VARIABLE LENGTH

            # tableswitch (170; 0xaa)
            case 170:
                i_initial = i
                switches = list()

                # Byte padding
                i += i % 4

                default = uint(bytes(code[i:i + 4]), signed=True)
                i += 4

                low = uint(bytes(code[i:i + 4]), signed=True)
                i += 4

                high = uint(bytes(code[i:i + 4]), signed=True)
                i += 4

                for _ in range(high - low + 1):
                    switches.append(uint(bytes(code[i:i + 4]), signed=True))
                    i += 4

                operations[i_initial] = ParsedOpcode(opcode.func_ref, (default, tuple(switches)))

            # tableswitch (171; 0xab)
            case 171:
                i_initial = i
                switches = dict[int, int]()

                # Byte padding
                i += i % 4

                default = uint(bytes(code[i:i + 4]), signed=True)
                i += 4

                npairs = uint(bytes(code[i:i + 4]), signed=True)
                i += 4

                for _ in range(npairs):
                    match = uint(bytes(code[i:i + 4]), signed=True)
                    i += 4
                    offset = uint(bytes(code[i:i + 4]), signed=True)
                    i += 4

                    switches[match] = offset

                operations[i_initial] = ParsedOpcode(opcode.func_ref, (default, tuple(switches)))

            # wide (196; 0xc4)
            case 196:
                i_initial = i
                params = list()

                i += 1
                mod_opcode = code[i]

                # Handle iinc
                param_count = 4 if mod_opcode == 132 else 2
                for j in range(1, param_count + 1):
                    params.append(code[i+j])
                i += param_count

                operations[i_initial] = ParsedOpcode(opcode.func_ref, (tuple(params)))

            # CONSTANT-LENGTH

            case _:
                params = list()

                for j in range(1, opcode.param_count + 1):
                    params.append(code[i+j])

                operations[i] = ParsedOpcode(opcode.func_ref, (tuple(params)))
                i += opcode.param_count + 1 if opcode.param_count > 0 else 1

    return operations


def parse_annotation(file):
    type_index = uint(file.read(2))
    num_element_value_pairs = uint(file.read(2))
    element_value_pairs = list()

    for _ in range(num_element_value_pairs):
        element_name_index = uint(file.read(2))
        element_value = parse_element_value(file)

        element_value_pairs.append(ElementValuePair(element_name_index, element_value))

    return Annotation(type_index, num_element_value_pairs, element_value_pairs)


def parse_typeannotation(file):
    target_type = hexlify(file.read(1)).decode("ascii")

    match target_type:
        case "00" | "01": target_info = TypeParameterTarget(uint(file.read(2)))
        case "10": target_info = SupertypeTarget(uint(file.read(2)))
        case "11" | "12": target_info = TypeParameterBoundTarget(
                uint(file.read(1)),
                uint(file.read(1))
            )
        case "13" | "14" | "15": target_info = EmptyTarget()
        case "16": target_info = FormalParameterTarget(uint(file.read(1)))
        case "17": target_info = ThrowsTarget(uint(file.read(2)))
        case "40" | "41":
            table_length = uint(file.read(2))
            table = list()

            for _ in range(table_length):
                table.append(LocalvarInfo(
                    uint(file.read(2)),
                    uint(file.read(2)),
                    uint(file.read(2))
                ))

            target_info = LocalvarTarget(table_length, table)
        case "42": target_info = CatchTarget(uint(file.read(2)))
        case "43" | "44" | "45" | "46": target_info = OffsetTarget(uint(file.read(2)))
        case "47" | "48" | "49" | "4A" | "4B": target_info = TypeArgumentTarget(
                uint(file.read(2)),
                uint(file.read(1))
            )
        case _:
            raise VerifyError(f"Failed to parse class: invalid target_type '{target_type}' in type annotation")

    path_length = uint(file.read(1))
    path = list()

    for _ in range(path_length):
        path.append(PathStep(
            uint(file.read(1)),
            uint(file.read(1))
        ))

    target_path = TypePath(path_length, path)
    type_index = uint(file.read(2))
    num_element_value_pairs = uint(file.read(2))
    element_value_pairs = list()

    for _ in range(num_element_value_pairs):
        element_name_index = uint(file.read(2))
        element_value = parse_element_value(file)

        element_value_pairs.append(ElementValuePair(element_name_index, element_value))

    return TypeAnnotation(
        target_type,
        target_info,
        target_path,
        type_index,
        num_element_value_pairs,
        element_value_pairs
    )


def parse_element_value(file) -> ElementValue:
    tag = file.read(1).decode("ascii")
    match tag:
        case "B": return ByteElementValue(uint(file.read(2)))
        case "C": return CharElementValue(uint(file.read(2)))
        case "D": return DoubleElementValue(uint(file.read(2)))
        case "F": return FloatElementValue(uint(file.read(2)))
        case "I": return IntElementValue(uint(file.read(2)))
        case "J": return LongElementValue(uint(file.read(2)))
        case "S": return ShortElementValue(uint(file.read(2)))
        case "Z": return ByteElementValue(uint(file.read(2)))
        case "s": return StringElementValue(uint(file.read(2)))
        case "s": return StringElementValue(uint(file.read(2)))
        case "e": return EnumElementValue(
                uint(file.read(2)),
                uint(file.read(2))
            )
        case "c": return ClassElementValue(uint(file.read(2)))
        case "@": return AnnotationElementValue(parse_annotation(file))
        case "[":
            num_values = uint(file.read(2))
            values = list()

            for _ in range(num_values):
                values.append(parse_element_value(file))

            return ArrayElementValue(num_values, values)
        case _: raise VerifyError(f"Failed to parse class: invalid element value union tag {tag}")


def parse_verification_type_info(file) -> VerificationTypeInfo:
    tag = uint(file.read(1))
    match tag:
        case 0: return TopVariableInfo()
        case 1: return IntegerVariableInfo()
        case 2: return FloatVariableInfo()
        case 3: return DoubleVariableInfo()
        case 4: return LongVariableInfo()
        case 5: return NullVariableInfo()
        case 6: return UninitializedThisVariableInfo()
        case 7: return ObjectVariableInfo(uint(file.read(2)))
        case 8: return UninitializedVariableInfo(uint(file.read(2)))
        case _: raise VerifyError(f"Failed to parse class: invalid verification type union tag {tag}")


# --------------------------------------------------
# FIELDS & METHODS
# --------------------------------------------------


def parse_field_method(file, method, constant_pool) -> Field | Method:
    access_flags = parse_method_flags(file) if method else parse_field_flags(file)
    name_index = uint(file.read(2))
    descriptor_index = uint(file.read(2))

    # Parse structure attributes
    attributes_count = uint(file.read(2))
    attribute_info = list()

    # Iterate through attributes
    for _ in range(attributes_count):
        attribute_name_index = uint(file.read(2))
        attribute_length = uint(file.read(4))

        attribute_info.append(parse_attribute(AttributeUnparsed(
            attribute_name_index,
            attribute_length
        ), file, constant_pool))

    return Method(
        access_flags,
        name_index,
        descriptor_index,
        attributes_count,
        attribute_info
    ) if method else Field(
        access_flags,
        name_index,
        descriptor_index,
        attributes_count,
        attribute_info
    )


# --------------------------------------------------
# ACCESS FLAGS
# --------------------------------------------------


def parse_class_flags(file) -> list[ClassFlags]:
    # TODO: Parse bit mask properly
    # hexlify(file.read(2)).decode("ascii")
    file.read(2)
    access_flags = list()
    return access_flags


def parse_method_flags(file) -> list[MethodFlags]:
    # hexlify(file.read(2)).decode("ascii")
    file.read(2)
    access_flags = list()
    return access_flags


def parse_field_flags(file)-> list[FieldFlags]:
    # hexlify(file.read(2)).decode("ascii")
    file.read(2)
    access_flags = list()
    return access_flags


def parse_method_parameter_flags(file) -> list[MethodParameterFlags]:
    file.read(2)
    access_flags = list()
    return access_flags


# --------------------------------------------------
# DATA TYPES
# --------------------------------------------------


def uint(bytez, signed=False) -> int:
    return int.from_bytes(bytez, byteorder="big", signed=signed)


def hex_(bytez) -> bytes:
    return hexlify(bytez)
