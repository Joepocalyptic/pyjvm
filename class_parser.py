from binascii import hexlify
from exceptions import ClassParseException
from objects import *


def parse(filename):
    file = open(filename, "rb")

    # All valid class files must start with 0xCAFEBABE
    if hexlify(file.read(4)) != b"cafebabe":
        file.close()
        raise ClassParseException(f"Failed to parse class {filename}: invalid magic number; likely not a class file")

    minor_version = int.from_bytes(file.read(2), byteorder="big")
    major_version = int.from_bytes(file.read(2), byteorder="big")

    # Currently only targeting class spec 52.0 (Java SE 8)
    if f"{major_version}.{minor_version}" != "52.0":
        file.close()
        raise ClassParseException(f"Failed to parse class {filename}: unsupported major/minor version {major_version}.{minor_version}")

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
        if entry is None:
            # Not in spec
            file.close()
            raise ClassParseException(f"Failed to parse class {filename}: invalid constant type {constant_type}")

        constant_pool.append(entry)

    # Decode access flag mask
    access_flags = parse_class_flags(hexlify(file.read(2)).decode("ascii"))

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
    if constant_type == 1:
        # ConstantUtf8Info
        length = int.from_bytes(file.read(2), byteorder="big")
        return ConstantUtf8Info(
            length,
            file.read(length)
        )
    elif constant_type == 3:
        # ConstantIntegerInfo
        return ConstantIntegerInfo(file.read(4))
    elif constant_type == 4:
        # ConstantFloatInfo
        return ConstantFloatInfo(file.read(4))
    elif constant_type == 5:
        # ConstantLongInfo
        return ConstantLongInfo(file.read(4), file.read(4))
    elif constant_type == 6:
        # ConstantDoubleInfo
        return ConstantLongInfo(file.read(4), file.read(4))
    elif constant_type == 7:
        # ConstantClassInfo
        return ConstantClassInfo(int.from_bytes(file.read(2), byteorder="big"))
    elif constant_type == 8:
        # ConstantStringInfo
        return ConstantStringInfo(int.from_bytes(file.read(2), byteorder="big"))
    elif constant_type == 9:
        # ConstantFieldrefInfo
        return ConstantFieldrefInfo(
            int.from_bytes(file.read(2), byteorder="big"),
            int.from_bytes(file.read(2), byteorder="big")
        )
    elif constant_type == 10:
        # ConstantMethodrefInfo
        return ConstantMethodrefInfo(
            int.from_bytes(file.read(2), byteorder="big"),
            int.from_bytes(file.read(2), byteorder="big")
        )
    elif constant_type == 11:
        # ConstantInterfaceMethodrefInfo
        return ConstantInterfaceMethodrefInfo(
            int.from_bytes(file.read(2), byteorder="big"),
            int.from_bytes(file.read(2), byteorder="big")
        )
    elif constant_type == 12:
        # ConstantNameAndTypeInfo
        return ConstantNameAndTypeInfo(
            int.from_bytes(file.read(2), byteorder="big"),
            int.from_bytes(file.read(2), byteorder="big")
        )
    elif constant_type == 15:
        # ConstantMethodHandleInfo
        return ConstantMethodHandleInfo(
            int.from_bytes(file.read(1), byteorder="big"),
            int.from_bytes(file.read(2), byteorder="big")
        )
    elif constant_type == 16:
        # ConstantMethodTypeInfo
        return ConstantMethodTypeInfo(int.from_bytes(file.read(2), byteorder="big"))
    elif constant_type == 18:
        # ConstantInvokeDynamicInfo
        return ConstantInvokeDynamicInfo(
            int.from_bytes(file.read(2), byteorder="big"),
            int.from_bytes(file.read(2), byteorder="big")
        )
    return None


def parse_attribute(attribute, file, constant_pool):
    attribute_name = constant_pool[attribute.attribute_name_index].bytes.decode("utf-8")

    if attribute_name == "ConstantValue":
        # ConstantValue
        return AttributeConstantValue(int.from_bytes(file.read(2), byteorder="big"))

    elif attribute_name == "Code":
        # Code
        max_stack = int.from_bytes(file.read(2), byteorder="big")
        max_locals = int.from_bytes(file.read(2), byteorder="big")
        code_length = int.from_bytes(file.read(4), byteorder="big")

        # TODO: Parse bytecode
        code = file.read(code_length)

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
            exception_table_length,
            exception_table,
            attributes_count,
            attribute_info
        )

    elif attribute_name == "StackMapTable":
        number_of_entries = int.from_bytes(file.read(2), byteorder="big")
        entries = list()

        for _ in range(number_of_entries):
            tag = int.from_bytes(file.read(1), byteorder="big")
            if 0 <= tag <= 63:
                entries.append(SameFrame(tag))
            elif 64 <= tag <= 127:
                stack = list()
                stack.append(parse_verification_type_info(file))

                entries.append(SameLocals1StackItemFrame(tag, stack))
            elif tag == 247:
                offset_delta = int.from_bytes(file.read(2), byteorder="big")

                stack = list()
                stack.append(parse_verification_type_info(file))

                entries.append(SameLocals1StackItemFrameExtended(tag, offset_delta, stack))
            elif 248 <= tag <= 250:
                offset_delta = int.from_bytes(file.read(2), byteorder="big")

                entries.append(ChopFrame(tag, offset_delta))
            elif tag == 251:
                offset_delta = int.from_bytes(file.read(2), byteorder="big")

                entries.append(SameFrameExtended(tag, offset_delta))
            elif 252 <= tag <= 254:
                offset_delta = int.from_bytes(file.read(2), byteorder="big")

                localz = list()
                for _ in range(tag-251):
                    # TODO: Double and long might need special treatment
                    localz.append(parse_verification_type_info(file))

                entries.append(AppendFrame(tag, offset_delta, localz))
            elif tag == 255:
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
            else:
                raise ClassParseException(f"Failed to parse class: invalid StackMapTable union tag {tag}")

        return AttributeStackMapTable(number_of_entries, entries)

    elif attribute_name == "Exceptions":
        number_of_exceptions = int.from_bytes(file.read(2), byteorder="big")
        exception_index_table = list()

        for _ in range(number_of_exceptions):
            exception_index_table.append(int.from_bytes(file.read(2), byteorder="big"))

        return AttributeExceptions(number_of_exceptions, exception_index_table)

    elif attribute_name == "InnerClasses":
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

    elif attribute_name == "EnclosingMethod":
        return AttributeEnclosingMethod(
            int.from_bytes(file.read(2), byteorder="big"),
            int.from_bytes(file.read(2), byteorder="big")
        )

    elif attribute_name == "Synthetic":
        return AttributeSynthetic()

    elif attribute_name == "Signature":
        # TODO: Parse signatures
        return AttributeSignature(
            int.from_bytes(file.read(2), byteorder="big")
        )

    elif attribute_name == "SourceFile":
        return AttributeSourceFile(
            int.from_bytes(file.read(2), byteorder="big")
        )

    elif attribute_name == "SourceDebugExtension":
        return AttributeSourceDebugExtension(file.read(attribute.attribute_length))

    elif attribute_name == "LineNumberTable":
        line_number_table_length = int.from_bytes(file.read(2), byteorder="big")
        line_number_table = list()

        for _ in range(line_number_table_length):
            line_number_table.append(LineNumber(
                int.from_bytes(file.read(2), byteorder="big"),
                int.from_bytes(file.read(2), byteorder="big")
            ))

        return AttributeLineNumberTable(line_number_table_length, line_number_table)

    elif attribute_name == "LocalVariableTable":
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

    elif attribute_name == "LocalVariableTypeTable":
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

    elif attribute_name == "Deprecated":
        return AttributeDeprecated()

    elif attribute_name == "RuntimeVisibleAnnotations":
        num_annotations = int.from_bytes(file.read(2), byteorder="big")
        annotations = list()

        for _ in range(num_annotations):
            annotations.append(parse_annotation(file))

        return AttributeRuntimeVisibleAnnotations(num_annotations, annotations)

    elif attribute_name == "RuntimeInvisibleAnnotations":
        num_annotations = int.from_bytes(file.read(2), byteorder="big")
        annotations = list()

        for _ in range(num_annotations):
            annotations.append(parse_annotation(file))

        return AttributeRuntimeInvisibleAnnotations(num_annotations, annotations)

    elif attribute_name == "RuntimeInvisibleAnnotations":
        num_annotations = int.from_bytes(file.read(2), byteorder="big")
        annotations = list()

        for _ in range(num_annotations):
            annotations.append(parse_annotation(file))

        return AttributeRuntimeInvisibleAnnotations(num_annotations, annotations)

    elif attribute_name == "RuntimeInvisibleParameterAnnotations":
        num_parameters = int.from_bytes(file.read(2), byteorder="big")
        parameter_annotations = list()

        for _ in range(num_parameters):
            num_annotations = int.from_bytes(file.read(2), byteorder="big")
            annotations = list()

            for _ in range(num_annotations):
                annotations.append(parse_annotation(file))

            parameter_annotations.append(ParameterAnnotations(num_annotations, annotations))

        return AttributeRuntimeInvisibleParameterAnnotations(num_parameters, parameter_annotations)

    elif attribute_name == "RuntimeVisibleTypeAnnotations":
        num_parameters = int.from_bytes(file.read(2), byteorder="big")
        parameter_annotations = list()

        for _ in range(num_parameters):
            num_annotations = int.from_bytes(file.read(2), byteorder="big")
            annotations = list()

            for _ in range(num_annotations):
                annotations.append(parse_annotation(file))

            parameter_annotations.append(ParameterAnnotations(num_annotations, annotations))

        return AttributeRuntimeVisibleParameterAnnotations(num_parameters, parameter_annotations)

    elif attribute_name == "RuntimeVisibleTypeAnnotations":
        # TODO: Everything
        pass

    else:
        # Not in spec; silently ignore and return ambiguous object
        return AttributeUnrecognized(
            attribute.attribute_name_index,
            attribute.attribute_length,
            file.read(attribute.attribute_length)
        )


def parse_annotation(file):
    type_index = int.from_bytes(file.read(2), byteorder="big")
    num_element_value_pairs = int.from_bytes(file.read(2), byteorder="big")
    element_value_pairs = list()

    for _ in range(num_element_value_pairs):
        element_name_index = int.from_bytes(file.read(2), byteorder="big")
        element_value = parse_element_value(file)

        element_value_pairs.append(ElementValuePair(element_name_index, element_value))

    return Annotation(type_index, num_element_value_pairs, element_value_pairs)


def parse_element_value(file):
    tag = file.read(1).decode("ascii")
    if tag == "B":
        return ByteElementValue(int.from_bytes(file.read(2), byteorder="big"))
    elif tag == "C":
        return CharElementValue(int.from_bytes(file.read(2), byteorder="big"))
    elif tag == "D":
        return DoubleElementValue(int.from_bytes(file.read(2), byteorder="big"))
    elif tag == "F":
        return FloatElementValue(int.from_bytes(file.read(2), byteorder="big"))
    elif tag == "I":
        return IntElementValue(int.from_bytes(file.read(2), byteorder="big"))
    elif tag == "J":
        return LongElementValue(int.from_bytes(file.read(2), byteorder="big"))
    elif tag == "S":
        return ShortElementValue(int.from_bytes(file.read(2), byteorder="big"))
    elif tag == "Z":
        return ByteElementValue(int.from_bytes(file.read(2), byteorder="big"))
    elif tag == "s":
        return StringElementValue(int.from_bytes(file.read(2), byteorder="big"))
    elif tag == "s":
        return StringElementValue(int.from_bytes(file.read(2), byteorder="big"))
    elif tag == "e":
        return EnumElementValue(
            int.from_bytes(file.read(2), byteorder="big"),
            int.from_bytes(file.read(2), byteorder="big")
        )
    elif tag == "c":
        return ClassElementValue(int.from_bytes(file.read(2), byteorder="big"))
    elif tag == "@":
        return parse_annotation(file)
    elif tag == "[":
        num_values = int.from_bytes(file.read(2), byteorder="big")
        values = list()

        for _ in range(num_values):
            values.append(parse_element_value(file))

        return ArrayElementValue(num_values, values)
    return


def parse_verification_type_info(file):
    tag = int.from_bytes(file.read(1), byteorder="big")
    if tag == 0:
        return TopVariableInfo()
    elif tag == 1:
        return IntegerVariableInfo()
    elif tag == 2:
        return FloatVariableInfo()
    elif tag == 3:
        return DoubleVariableInfo()
    elif tag == 4:
        return LongVariableInfo()
    elif tag == 5:
        return NullVariableInfo()
    elif tag == 6:
        return UninitializedThisVariableInfo()
    elif tag == 7:
        return ObjectVariableInfo(int.from_bytes(file.read(2), byteorder="big"))
    elif tag == 8:
        return UninitializedVariableInfo(int.from_bytes(file.read(2), byteorder="big"))
    else:
        # Not in spec
        raise ClassParseException(f"Failed to parse class: invalid verification type union tag {tag}")


def parse_field_method(file, method, constant_pool):
    access_flags = hexlify(file.read(2)).decode("ascii")
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


def parse_class_flags(mask):
    # TODO: Parse bit mask properly
    access_flags = list()
    return access_flags
