import objects
from exceptions import ClassParseException
from binascii import hexlify
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
        interfaces.append(ConstantClassInfo(int.from_bytes(file.read(2), byteorder="big")))
        interfaces_count_iter -= 1

    # Parse fields
    fields_count = int.from_bytes(file.read(2), byteorder="big")
    fields_count_iter = fields_count
    fields = list()

    # Iterate through fields
    while fields_count_iter > 0:

        fields_count_iter -= 1

    file.close()


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


def parse_class_flags(mask):
    access_flags = list()
    if mask[0] == '1':
        access_flags.append(ClassFlags.ACC_SYNTHETIC)
    elif mask[0] == '2':
        access_flags.append(ClassFlags.ACC_ANNOTATION)
    elif mask[0] == '4':
        access_flags.append(ClassFlags.ACC_ENUM)

    if mask[1] == '2':
        access_flags.append(ClassFlags.ACC_INTERFACE)
    elif mask[1] == '4':
        access_flags.append(ClassFlags.ACC_ABSTRACT)

    if mask[2] == '1':
        access_flags.append(ClassFlags.ACC_FINAL)
    elif mask[2] == '2':
        access_flags.append(ClassFlags.ACC_SUPER)

    if mask[3] == "1":
        access_flags.append(ClassFlags.ACC_PUBLIC)

    return access_flags
