from dataclasses import dataclass


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