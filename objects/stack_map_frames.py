from dataclasses import dataclass

from objects.type_verification import VerificationTypeInfo


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