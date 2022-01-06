from dataclasses import dataclass


@dataclass
class Frame:
    local_vars = list
    operand_stack = list
    constant_pool = list
