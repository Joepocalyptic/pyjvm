from binascii import hexlify
from exceptions import ClassParseException
from objects import *
from opcodes import opcodes, Opcode


def parse(filename):
    file = open(filename, "rb")

    # All valid class files must start with 0xCAFEBABE
    if hexlify(file.read(4)) != b"cafebabe":
        file.close()
        raise ClassParseException(f"Failed to parse class: invalid magic number; likely not a class file")

    minor_version = int.from_bytes(file.read(2), byteorder="big")
    major_version = int.from_bytes(file.read(2), byteorder="big")

    # Currently only targeting class spec 52.0 (Java SE 8)
    if f"{major_version}.{minor_version}" != "52.0":
        file.close()
        raise ClassParseException(f"Failed to parse class: unsupported major/minor version {major_version}.{minor_version}")

    # Parse constant pool
    constant_pool_count = int.from_bytes(file.read(2), byteorder="big")
    constant_pool = list()

    # noinspection PyTypeChecker
    # Bump to 1-indexed list
    constant_pool.append(None)

    # Iterate through constant pool
    pool_count = constant_pool_count-1
    for _ in range(pool_count):
        constant_type = int.from_bytes(file.read(1), byteorder="big")
        entry = parse_constant_pool_entry(file, constant_type)
        constant_pool.append(entry)

    # Decode access flag mask
    access_flags = parse_class_flags(file)

    this_class = int.from_bytes(file.read(2), byteorder="big")
    super_class = int.from_bytes(file.read(2), byteorder="big")

    # Parse superinterfaces
    interfaces_count = int.from_bytes(file.read(2), byteorder="big")
    interfaces = list()

    # Iterate through superinterfaces
    for _ in range(interfaces_count):
        interfaces.append(int.from_bytes(file.read(2), byteorder="big"))

    # Parse fields
    fields_count = int.from_bytes(file.read(2), byteorder="big")
    fields = list()

    # Iterate through fields
    for _ in range(fields_count):
        fields.append(parse_field_method(file, False, constant_pool))

    # Parse methods
    methods_count = int.from_bytes(file.read(2), byteorder="big")
    methods = list()

    # Iterate through methods
    for _ in range(methods_count):
        methods.append(parse_field_method(file, True, constant_pool))

    # Parse class attributes
    attributes_count = int.from_bytes(file.read(2), byteorder="big")
    attribute_info = list()

    # Iterate through attributes
    for _ in range(attributes_count):
        attribute_name_index = int.from_bytes(file.read(2), byteorder="big")
        attribute_length = int.from_bytes(file.read(4), byteorder="big")

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
            length = int.from_bytes(file.read(2), byteorder="big")
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
            return ConstantClassInfo(int.from_bytes(file.read(2), byteorder="big"))
        case 8:
            return ConstantStringInfo(int.from_bytes(file.read(2), byteorder="big"))
        case 9:
            return ConstantFieldrefInfo(
                int.from_bytes(file.read(2), byteorder="big"),
                int.from_bytes(file.read(2), byteorder="big")
            )
        case 10:
            return ConstantMethodrefInfo(
                int.from_bytes(file.read(2), byteorder="big"),
                int.from_bytes(file.read(2), byteorder="big")
            )
        case 11:
            return ConstantInterfaceMethodrefInfo(
                int.from_bytes(file.read(2), byteorder="big"),
                int.from_bytes(file.read(2), byteorder="big")
            )
        case 12:
            return ConstantNameAndTypeInfo(
                int.from_bytes(file.read(2), byteorder="big"),
                int.from_bytes(file.read(2), byteorder="big")
            )
        case 15:
            return ConstantMethodHandleInfo(
                int.from_bytes(file.read(1), byteorder="big"),
                int.from_bytes(file.read(2), byteorder="big")
            )
        case 16:
            return ConstantMethodTypeInfo(int.from_bytes(file.read(2), byteorder="big"))
        case 18:
            return ConstantInvokeDynamicInfo(
                int.from_bytes(file.read(2), byteorder="big"),
                int.from_bytes(file.read(2), byteorder="big")
            )
        case _:
            raise ClassParseException(f"Failed to parse class: invalid constant type {constant_type}")


def parse_attribute(attribute, file, constant_pool):
    attribute_name = constant_pool[attribute.attribute_name_index].bytes.decode("utf-8")
    match attribute_name:
        case "ConstantValue":
            return AttributeConstantValue(int.from_bytes(file.read(2), byteorder="big"))

        case "Code":
            max_stack = int.from_bytes(file.read(2), byteorder="big")
            max_locals = int.from_bytes(file.read(2), byteorder="big")
            code_length = int.from_bytes(file.read(4), byteorder="big")

            # TODO: Parse bytecode
            code = file.read(code_length)
            parsed_code = parse_bytecode(code)

            exception_table_length = int.from_bytes(file.read(2), byteorder="big")
            exception_table = list()

            for _ in range(exception_table_length):
                exception_table.append(ExceptionHandler(
                    int.from_bytes(file.read(2), byteorder="big"),
                    int.from_bytes(file.read(2), byteorder="big"),
                    int.from_bytes(file.read(2), byteorder="big"),
                    int.from_bytes(file.read(2), byteorder="big")
                ))

            attributes_count = int.from_bytes(file.read(2), byteorder="big")
            attribute_info = list()

            # Iterate through nested attributes
            for _ in range(attributes_count):
                attribute_name_index = int.from_bytes(file.read(2), byteorder="big")
                attribute_length = int.from_bytes(file.read(4), byteorder="big")

                attribute_info.append(parse_attribute(AttributeUnparsed(
                    attribute_name_index,
                    attribute_length
                ), file, constant_pool))

            return AttributeCode(
                max_stack,
                max_locals,
                code_length,
                code,
                parsed_code,
                exception_table_length,
                exception_table,
                attributes_count,
                attribute_info
            )

        case "StackMapTable":
            number_of_entries = int.from_bytes(file.read(2), byteorder="big")
            entries = list()

            for _ in range(number_of_entries):
                tag = int.from_bytes(file.read(1), byteorder="big")
                match tag:
                    case tag if tag in range(0, 64):
                        entries.append(SameFrame(tag))
                    case tag if tag in range(64, 128):
                        stack = list()
                        stack.append(parse_verification_type_info(file))

                        entries.append(SameLocals1StackItemFrame(tag, stack))
                    case tag if tag == 247:
                        offset_delta = int.from_bytes(file.read(2), byteorder="big")

                        stack = list()
                        stack.append(parse_verification_type_info(file))

                        entries.append(SameLocals1StackItemFrameExtended(tag, offset_delta, stack))
                    case tag if tag in range(248, 251):
                        offset_delta = int.from_bytes(file.read(2), byteorder="big")

                        entries.append(ChopFrame(tag, offset_delta))
                    case tag if tag == 251:
                        offset_delta = int.from_bytes(file.read(2), byteorder="big")

                        entries.append(SameFrameExtended(tag, offset_delta))
                    case tag if tag in range(252, 255):
                        offset_delta = int.from_bytes(file.read(2), byteorder="big")

                        localz = list()
                        for _ in range(tag-251):
                            # TODO: Double and long might need special treatment
                            localz.append(parse_verification_type_info(file))

                        entries.append(AppendFrame(tag, offset_delta, localz))
                    case tag if tag == 255:
                        offset_delta = int.from_bytes(file.read(2), byteorder="big")

                        number_of_locals = int.from_bytes(file.read(2), byteorder="big")
                        localz = list()
                        for _ in range(number_of_locals):
                            localz.append(parse_verification_type_info(file))

                        number_of_stack_items = int.from_bytes(file.read(2), byteorder="big")
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
                    case _:
                        raise ClassParseException(f"Failed to parse class: invalid StackMapTable union tag {tag}")

            return AttributeStackMapTable(number_of_entries, entries)

        case "Exceptions":
            number_of_exceptions = int.from_bytes(file.read(2), byteorder="big")
            exception_index_table = list()

            for _ in range(number_of_exceptions):
                exception_index_table.append(int.from_bytes(file.read(2), byteorder="big"))

            return AttributeExceptions(number_of_exceptions, exception_index_table)

        case "InnerClasses":
            number_of_classes = int.from_bytes(file.read(2), byteorder="big")
            classes = list()

            for _ in range(number_of_classes):
                classes.append(InnerClassEntry(
                    int.from_bytes(file.read(2), byteorder="big"),
                    int.from_bytes(file.read(2), byteorder="big"),
                    int.from_bytes(file.read(2), byteorder="big"),
                    int.from_bytes(file.read(2), byteorder="big")
                ))

            return AttributeInnerClasses(number_of_classes, classes)

        case "EnclosingMethod":
            return AttributeEnclosingMethod(
                int.from_bytes(file.read(2), byteorder="big"),
                int.from_bytes(file.read(2), byteorder="big")
            )

        case "Synthetic":
            return AttributeSynthetic()

        case "Signature":
            # TODO: Parse signatures
            return AttributeSignature(
                int.from_bytes(file.read(2), byteorder="big")
            )

        case "SourceFile":
            return AttributeSourceFile(
                int.from_bytes(file.read(2), byteorder="big")
            )

        case "SourceDebugExtension":
            return AttributeSourceDebugExtension(file.read(attribute.attribute_length))

        case "LineNumberTable":
            line_number_table_length = int.from_bytes(file.read(2), byteorder="big")
            line_number_table = list()

            for _ in range(line_number_table_length):
                line_number_table.append(LineNumber(
                    int.from_bytes(file.read(2), byteorder="big"),
                    int.from_bytes(file.read(2), byteorder="big")
                ))

            return AttributeLineNumberTable(line_number_table_length, line_number_table)

        case "LocalVariableTable":
            local_variable_table_length = int.from_bytes(file.read(2), byteorder="big")
            local_variable_table = list()

            for _ in range(local_variable_table_length):
                local_variable_table.append(LocalVariable(
                    int.from_bytes(file.read(2), byteorder="big"),
                    int.from_bytes(file.read(2), byteorder="big"),
                    int.from_bytes(file.read(2), byteorder="big"),
                    int.from_bytes(file.read(2), byteorder="big"),
                    int.from_bytes(file.read(2), byteorder="big")
                ))

            return AttributeLocalVariableTable(local_variable_table_length, local_variable_table)

        case "LocalVariableTypeTable":
            local_variable_type_table_length = int.from_bytes(file.read(2), byteorder="big")
            local_variable_type_table = list()

            for _ in range(local_variable_type_table_length):
                local_variable_type_table.append(LocalVariableType(
                    int.from_bytes(file.read(2), byteorder="big"),
                    int.from_bytes(file.read(2), byteorder="big"),
                    int.from_bytes(file.read(2), byteorder="big"),
                    int.from_bytes(file.read(2), byteorder="big"),
                    int.from_bytes(file.read(2), byteorder="big")
                ))

            return AttributeLocalVariableTypeTable(local_variable_type_table_length, local_variable_type_table)

        case "Deprecated":
            return AttributeDeprecated()

        case "RuntimeVisibleAnnotations":
            num_annotations = int.from_bytes(file.read(2), byteorder="big")
            annotations = list()

            for _ in range(num_annotations):
                annotations.append(parse_annotation(file))

            return AttributeRuntimeVisibleAnnotations(num_annotations, annotations)

        case "RuntimeInvisibleAnnotations":
            num_annotations = int.from_bytes(file.read(2), byteorder="big")
            annotations = list()

            for _ in range(num_annotations):
                annotations.append(parse_annotation(file))

            return AttributeRuntimeInvisibleAnnotations(num_annotations, annotations)

        case "RuntimeVisibleParameterAnnotations":
            num_parameters = int.from_bytes(file.read(2), byteorder="big")
            parameter_annotations = list()

            for _ in range(num_parameters):
                num_annotations = int.from_bytes(file.read(2), byteorder="big")
                annotations = list()

                for _ in range(num_annotations):
                    annotations.append(parse_annotation(file))

                parameter_annotations.append(ParameterAnnotations(num_annotations, annotations))

            return AttributeRuntimeVisibleParameterAnnotations(num_parameters, parameter_annotations)

        case "RuntimeInvisibleParameterAnnotations":
            num_parameters = int.from_bytes(file.read(2), byteorder="big")
            parameter_annotations = list()

            for _ in range(num_parameters):
                num_annotations = int.from_bytes(file.read(2), byteorder="big")
                annotations = list()

                for _ in range(num_annotations):
                    annotations.append(parse_annotation(file))

                parameter_annotations.append(ParameterAnnotations(num_annotations, annotations))

            return AttributeRuntimeInvisibleParameterAnnotations(num_parameters, parameter_annotations)

        case "RuntimeVisibleTypeAnnotations":
            num_annotations = int.from_bytes(file.read(2), byteorder="big")
            annotations = list()

            for _ in range(num_annotations):
                annotations.append(parse_typeannotation(file))

            return AttributeRuntimeVisibleTypeAnnotations(num_annotations, annotations)

        case "RuntimeInvisibleTypeAnnotations":
            num_annotations = int.from_bytes(file.read(2), byteorder="big")
            annotations = list()

            for _ in range(num_annotations):
                annotations.append(parse_typeannotation(file))

            return AttributeRuntimeInvisibleTypeAnnotations(num_annotations, annotations)

        case "AnnotationDefault":
            return AttributeAnnotationDefault(parse_element_value(file))

        case "BootstrapMethods":
            num_bootstrap_methods = int.from_bytes(file.read(2), byteorder="big")
            bootstrap_methods = list()

            for _ in range(num_bootstrap_methods):
                bootstrap_method_ref = int.from_bytes(file.read(2), byteorder="big")
                num_bootstrap_arguments = int.from_bytes(file.read(2), byteorder="big")
                bootstrap_arguments = list()

                for _ in range(num_bootstrap_arguments):
                    bootstrap_arguments.append(int.from_bytes(file.read(2), byteorder="big"))

                bootstrap_methods.append(BootstrapMethod(
                    bootstrap_method_ref,
                    num_bootstrap_arguments,
                    bootstrap_arguments
                ))

            return AttributeBootstrapMethods(num_bootstrap_methods, bootstrap_methods)

        case "MethodParameters":
            parameters_count = int.from_bytes(file.read(1), byteorder="big")
            parameters = list()

            for _ in range(parameters_count):
                parameters.append(MethodParameter(
                    int.from_bytes(file.read(2), byteorder="big"),
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
    print(code)
    return list()


def parse_annotation(file):
    type_index = int.from_bytes(file.read(2), byteorder="big")
    num_element_value_pairs = int.from_bytes(file.read(2), byteorder="big")
    element_value_pairs = list()

    for _ in range(num_element_value_pairs):
        element_name_index = int.from_bytes(file.read(2), byteorder="big")
        element_value = parse_element_value(file)

        element_value_pairs.append(ElementValuePair(element_name_index, element_value))

    return Annotation(type_index, num_element_value_pairs, element_value_pairs)


def parse_typeannotation(file):
    target_type = hexlify(file.read(1)).decode("ascii")

    match target_type:
        case "00" | "01": target_info = TypeParameterTarget(int.from_bytes(file.read(2), byteorder="big"))
        case "10": target_info = SupertypeTarget(int.from_bytes(file.read(2), byteorder="big"))
        case "11" | "12": target_info = TypeParameterBoundTarget(
                int.from_bytes(file.read(1), byteorder="big"),
                int.from_bytes(file.read(1), byteorder="big")
            )
        case "13" | "14" | "15": target_info = EmptyTarget()
        case "16": target_info = FormalParameterTarget(int.from_bytes(file.read(1), byteorder="big"))
        case "17": target_info = ThrowsTarget(int.from_bytes(file.read(2), byteorder="big"))
        case "40" | "41":
            table_length = int.from_bytes(file.read(2), byteorder="big")
            table = list()

            for _ in range(table_length):
                table.append(LocalvarInfo(
                    int.from_bytes(file.read(2), byteorder="big"),
                    int.from_bytes(file.read(2), byteorder="big"),
                    int.from_bytes(file.read(2), byteorder="big")
                ))

            target_info = LocalvarTarget(table_length, table)
        case "42": target_info = CatchTarget(int.from_bytes(file.read(2), byteorder="big"))
        case "43" | "44" | "45" | "46": target_info = OffsetTarget(int.from_bytes(file.read(2), byteorder="big"))
        case "47" | "48" | "49" | "4A" | "4B": target_info = TypeArgumentTarget(
                int.from_bytes(file.read(2), byteorder="big"),
                int.from_bytes(file.read(1), byteorder="big")
            )
        case _:
            raise ClassParseException(f"Failed to parse class: invalid target_type '{target_type}' in type annotation")

    path_length = int.from_bytes(file.read(1), byteorder="big")
    path = list()

    for _ in range(path_length):
        path.append(PathStep(
            int.from_bytes(file.read(1), byteorder="big"),
            int.from_bytes(file.read(1), byteorder="big")
        ))

    target_path = TypePath(path_length, path)
    type_index = int.from_bytes(file.read(2), byteorder="big")
    num_element_value_pairs = int.from_bytes(file.read(2), byteorder="big")
    element_value_pairs = list()

    for _ in range(num_element_value_pairs):
        element_name_index = int.from_bytes(file.read(2), byteorder="big")
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


def parse_element_value(file):
    tag = file.read(1).decode("ascii")
    match tag:
        case "B": return ByteElementValue(int.from_bytes(file.read(2), byteorder="big"))
        case "C": return CharElementValue(int.from_bytes(file.read(2), byteorder="big"))
        case "D": return DoubleElementValue(int.from_bytes(file.read(2), byteorder="big"))
        case "F": return FloatElementValue(int.from_bytes(file.read(2), byteorder="big"))
        case "I": return IntElementValue(int.from_bytes(file.read(2), byteorder="big"))
        case "J": return LongElementValue(int.from_bytes(file.read(2), byteorder="big"))
        case "S": return ShortElementValue(int.from_bytes(file.read(2), byteorder="big"))
        case "Z": return ByteElementValue(int.from_bytes(file.read(2), byteorder="big"))
        case "s": return StringElementValue(int.from_bytes(file.read(2), byteorder="big"))
        case "s": return StringElementValue(int.from_bytes(file.read(2), byteorder="big"))
        case "e": return EnumElementValue(
                int.from_bytes(file.read(2), byteorder="big"),
                int.from_bytes(file.read(2), byteorder="big")
            )
        case "c": return ClassElementValue(int.from_bytes(file.read(2), byteorder="big"))
        case "@": return parse_annotation(file)
        case "[":
            num_values = int.from_bytes(file.read(2), byteorder="big")
            values = list()

            for _ in range(num_values):
                values.append(parse_element_value(file))

            return ArrayElementValue(num_values, values)
        case _: raise ClassParseException(f"Failed to parse class: invalid element value union tag {tag}")


def parse_verification_type_info(file):
    tag = int.from_bytes(file.read(1), byteorder="big")
    match tag:
        case 0: return TopVariableInfo()
        case 1: return IntegerVariableInfo()
        case 2: return FloatVariableInfo()
        case 3: return DoubleVariableInfo()
        case 4: return LongVariableInfo()
        case 5: return NullVariableInfo()
        case 6: return UninitializedThisVariableInfo()
        case 7: return ObjectVariableInfo(int.from_bytes(file.read(2), byteorder="big"))
        case 8: return UninitializedVariableInfo(int.from_bytes(file.read(2), byteorder="big"))
        case _: raise ClassParseException(f"Failed to parse class: invalid verification type union tag {tag}")


def parse_field_method(file, method, constant_pool):
    access_flags = parse_method_flags(file) if method else parse_field_flags(file)
    name_index = int.from_bytes(file.read(2), byteorder="big")
    descriptor_index = int.from_bytes(file.read(2), byteorder="big")

    # Parse structure attributes
    attributes_count = int.from_bytes(file.read(2), byteorder="big")
    attribute_info = list()

    # Iterate through attributes
    for _ in range(attributes_count):
        attribute_name_index = int.from_bytes(file.read(2), byteorder="big")
        attribute_length = int.from_bytes(file.read(4), byteorder="big")

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


def parse_class_flags(file):
    # TODO: Parse bit mask properly
    # hexlify(file.read(2)).decode("ascii")
    file.read(2)
    access_flags = list()
    return access_flags


def parse_method_flags(file):
    # hexlify(file.read(2)).decode("ascii")
    file.read(2)
    access_flags = list()
    return access_flags


def parse_field_flags(file):
    # hexlify(file.read(2)).decode("ascii")
    file.read(2)
    access_flags = list()
    return access_flags


def parse_method_parameter_flags(file):
    file.read(2)
    access_flags = list()
    return access_flags
