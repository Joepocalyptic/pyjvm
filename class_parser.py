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
    print(AttributeConstantValue)

    # Parse constant pool
    constant_pool_count = int.from_bytes(file.read(2), byteorder="big")
    constant_pool = list()

    # noinspection PyTypeChecker
    # Bump to 1-indexed list
    constant_pool.append(None)

    # Iterate through constant pool
    pool_count = constant_pool_count-1
    while pool_count > 0:
        constant_type = int.from_bytes(file.read(1), byteorder="big")

        entry = parse_constant_pool_entry(file, constant_type)
        if entry is None:
            # Not in spec
            file.close()
            raise ClassParseException(f"Failed to parse class {filename}: invalid constant type {constant_type}")

        constant_pool.append(entry)
        pool_count -= 1

    # Decode access flag mask
    access_flags = parse_class_flags(hexlify(file.read(2)).decode("ascii"))

    this_class = int.from_bytes(file.read(2), byteorder="big")
    super_class = int.from_bytes(file.read(2), byteorder="big")

    # Parse superinterfaces
    interfaces_count = int.from_bytes(file.read(2), byteorder="big")
    interfaces_count_iter = interfaces_count
    interfaces = list()

    # Iterate through superinterfaces
    while interfaces_count_iter > 0:
        interfaces.append(int.from_bytes(file.read(2), byteorder="big"))
        interfaces_count_iter -= 1

    # Parse fields
    fields_count = int.from_bytes(file.read(2), byteorder="big")
    fields_count_iter = fields_count
    fields = list()

    # Iterate through fields
    while fields_count_iter > 0:
        fields.append(parse_field_method(file, False, constant_pool))
        fields_count_iter -= 1

    # Parse methods
    methods_count = int.from_bytes(file.read(2), byteorder="big")
    methods_count_iter = methods_count
    methods = list()

    # Iterate through methods
    while methods_count_iter > 0:
        methods.append(parse_field_method(file, True, constant_pool))
        methods_count_iter -= 1

    # Parse class attributes
    attributes_count = int.from_bytes(file.read(2), byteorder="big")
    attributes_count_iter = attributes_count
    attribute_info = list()

    # Iterate through attributes
    while attributes_count_iter > 0:
        attribute_name_index = int.from_bytes(file.read(2), byteorder="big")
        attribute_length = int.from_bytes(file.read(4), byteorder="big")
        info = file.read(attribute_length)

        attribute_info.append(AttributeUnrecognized(
            attribute_name_index,
            attribute_length,
            info
        ))
        attributes_count_iter -= 1

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
        exception_table_length_iter = exception_table_length

        while exception_table_length_iter > 0:
            exception_table.append(ExceptionHandler(
                int.from_bytes(file.read(2), byteorder="big"),
                int.from_bytes(file.read(2), byteorder="big"),
                int.from_bytes(file.read(2), byteorder="big"),
                int.from_bytes(file.read(2), byteorder="big")
            ))
            exception_table_length -= 1

        attributes_count = int.from_bytes(file.read(2), byteorder="big")
        attributes_count_iter = attributes_count
        attribute_info = list()

        # Iterate through nested attributes
        while attributes_count_iter > 0:
            attribute_name_index = int.from_bytes(file.read(2), byteorder="big")
            attribute_length = int.from_bytes(file.read(4), byteorder="big")

            attribute_info.append(parse_attribute(AttributeUnparsed(
                attribute_name_index,
                attribute_length
            ), file, constant_pool))
            attributes_count_iter -= 1

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
    elif attribute_name == "":
        return
    elif attribute_name == "":
        return
    elif attribute_name == "":
        return
    elif attribute_name == "":
        return
    elif attribute_name == "":
        return
    elif attribute_name == "":
        return
    elif attribute_name == "":
        return
    elif attribute_name == "":
        return
    elif attribute_name == "":
        return
    elif attribute_name == "":
        return
    elif attribute_name == "":
        return
    else:
        # Not in spec; silently ignore and return ambiguous object
        return AttributeUnrecognized(
            attribute.attribute_name_index,
            attribute.attribute_length,
            file.read(attribute.attribute_length)
        )


def parse_field_method(file, method, constant_pool):
    access_flags = hexlify(file.read(2)).decode("ascii")
    name_index = int.from_bytes(file.read(2), byteorder="big")
    descriptor_index = int.from_bytes(file.read(2), byteorder="big")

    # Parse structure attributes
    attributes_count = int.from_bytes(file.read(2), byteorder="big")
    attributes_count_iter = attributes_count
    attribute_info = list()

    # Iterate through attributes
    while attributes_count_iter > 0:
        attribute_name_index = int.from_bytes(file.read(2), byteorder="big")
        attribute_length = int.from_bytes(file.read(4), byteorder="big")

        attribute_info.append(parse_attribute(AttributeUnparsed(
            attribute_name_index,
            attribute_length
        ), file, constant_pool))
        attributes_count_iter -= 1

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
