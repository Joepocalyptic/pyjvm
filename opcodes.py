from dataclasses import dataclass


@dataclass
class Opcode:
    func_ref: callable
    param_count: int


@dataclass
class ParsedOpcode:
    func_ref: callable
    params: list[any]


opcodes = {}


def opcode(code, param_bytes=0):
    def decorator(func):
        opcodes[code] = Opcode(func, param_bytes)

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


@opcode(50)
def aaload():
    pass


@opcode(83)
def aastore():
    pass


@opcode(1)
def aconst_null():
    pass


@opcode(25, 1)
def aload():
    pass


@opcode(42)
def aload_0():
    pass


@opcode(43)
def aload_1():
    pass


@opcode(44)
def aload_2():
    pass


@opcode(45)
def aload_3():
    pass


@opcode(189, 2)
def anewarray():
    pass


@opcode(176)
def areturn():
    pass


@opcode(190)
def arraylength():
    pass


@opcode(58, 1)
def astore():
    pass


@opcode(75)
def astore_0():
    pass


@opcode(76)
def astore_1():
    pass


@opcode(77)
def astore_2():
    pass


@opcode(78)
def astore_3():
    pass


@opcode(191)
def athrow():
    pass


@opcode(51)
def baload():
    pass


@opcode(84)
def bastore():
    pass


@opcode(16, 1)
def bipush():
    pass


@opcode(52)
def caload():
    pass


@opcode(85)
def castore():
    pass


@opcode(192, 2)
def checkcast():
    pass


@opcode(144)
def d2f():
    pass


@opcode(142)
def d2i():
    pass


@opcode(143)
def d2l():
    pass


@opcode(99)
def dadd():
    pass


@opcode(49)
def daload():
    pass


@opcode(82)
def dastore():
    pass


@opcode(152)
def dcmpg():
    pass


@opcode(151)
def dcmpl():
    pass


@opcode(14)
def dconst_0():
    pass


@opcode(15)
def dconst_1():
    pass


@opcode(111)
def ddiv():
    pass


@opcode(24, 1)
def dload():
    pass


@opcode(38)
def dload_0():
    pass


@opcode(39)
def dload_1():
    pass


@opcode(40)
def dload_2():
    pass


@opcode(41)
def dload_3():
    pass


@opcode(107)
def dmul():
    pass


@opcode(119)
def dneg():
    pass


@opcode(115)
def drem():
    pass


@opcode(175)
def dreturn():
    pass


@opcode(57, 1)
def dstore():
    pass


@opcode(71)
def dstore_0():
    pass


@opcode(72)
def dstore_1():
    pass


@opcode(73)
def dstore_2():
    pass


@opcode(74)
def dstore_3():
    pass


@opcode(103)
def dsub():
    pass


@opcode(89)
def dup():
    pass


@opcode(90)
def dup_x1():
    pass


@opcode(91)
def dup_x2():
    pass


@opcode(92)
def dup2():
    pass


@opcode(93)
def dup2_x1():
    pass


@opcode(94)
def dup2_x2():
    pass


@opcode(141)
def f2d():
    pass


@opcode(139)
def f2i():
    pass


@opcode(140)
def f2l():
    pass


@opcode(98)
def fadd():
    pass


@opcode(48)
def faload():
    pass


@opcode(81)
def fastore():
    pass


@opcode(150)
def fcmpg():
    pass


@opcode(149)
def fcmpl():
    pass


@opcode(11)
def fconst_0():
    pass


@opcode(12)
def fconst_1():
    pass


@opcode(13)
def fconst_2():
    pass


@opcode(110)
def fdiv():
    pass


@opcode(23, 1)
def fload():
    pass


@opcode(34)
def fload_0():
    pass


@opcode(35)
def fload_1():
    pass


@opcode(36)
def fload_2():
    pass


@opcode(37)
def fload_3():
    pass


@opcode(106)
def fmul():
    pass


@opcode(118)
def fneg():
    pass


@opcode(114)
def frem():
    pass


@opcode(174)
def freturn():
    pass


@opcode(56, 1)
def fstore():
    pass


@opcode(67)
def fstore_0():
    pass


@opcode(68)
def fstore_1():
    pass


@opcode(69)
def fstore_2():
    pass


@opcode(70)
def fstore_3():
    pass


@opcode(102)
def fsub():
    pass


@opcode(180, 2)
def getfield():
    pass


@opcode(178, 2)
def getstatic():
    pass


@opcode(167, 2)
def goto():
    pass


@opcode(200, 4)
def goto_w():
    pass


@opcode(145)
def i2b():
    pass


@opcode(145)
def i2c():
    pass


@opcode(135)
def i2d():
    pass


@opcode(134)
def i2f():
    pass


@opcode(133)
def i2l():
    pass


@opcode(147)
def i2s():
    pass


@opcode(96)
def iadd():
    pass


@opcode(46)
def iaload():
    pass


@opcode(126)
def iand():
    pass


@opcode(79)
def iastore():
    pass


@opcode(2)
def iconst_m1():
    pass


@opcode(3)
def iconst_0():
    pass


@opcode(4)
def iconst_1():
    pass


@opcode(5)
def iconst_2():
    pass


@opcode(6)
def iconst_3():
    pass


@opcode(7)
def iconst_4():
    pass


@opcode(8)
def iconst_5():
    pass


@opcode(108)
def idiv():
    pass


@opcode(165, 2)
def if_acmpeq():
    pass


@opcode(166, 2)
def if_acmpne():
    pass


@opcode(159, 2)
def if_icmpeq():
    pass


@opcode(160, 2)
def if_icmpne():
    pass


@opcode(161, 2)
def if_icmplt():
    pass


@opcode(162, 2)
def if_icmpge():
    pass


@opcode(163, 2)
def if_icmpgt():
    pass


@opcode(164, 2)
def if_icmple():
    pass


@opcode(153, 2)
def ifeq():
    pass


@opcode(154, 2)
def ifne():
    pass


@opcode(155, 2)
def iflt():
    pass


@opcode(156, 2)
def ifge():
    pass


@opcode(157, 2)
def ifgt():
    pass


@opcode(158, 2)
def ifle():
    pass


@opcode(199, 2)
def ifnonnull():
    pass


@opcode(198, 2)
def ifnull():
    pass


@opcode(132, 2)
def iinc():
    pass


@opcode(21, 1)
def iload():
    pass


@opcode(26)
def iload_0():
    pass


@opcode(27)
def iload_1():
    pass


@opcode(28)
def iload_2():
    pass


@opcode(29)
def iload_3():
    pass


@opcode(104)
def imul():
    pass


@opcode(116)
def ineg():
    pass


@opcode(193, 2)
def instanceof():
    pass


@opcode(186, 4)
def invokedynamic():
    pass


@opcode(185, 4)
def invokeinterface():
    pass


@opcode(183, 2)
def invokespecial():
    pass


@opcode(184, 2)
def invokestatic():
    pass


@opcode(182, 2)
def invokevirtual():
    pass


@opcode(128)
def ior():
    pass


@opcode(112)
def irem():
    pass


@opcode(172)
def ireturn():
    pass


@opcode(120)
def ishl():
    pass


@opcode(122)
def ishr():
    pass


@opcode(54, 1)
def istore():
    pass


@opcode(59)
def istore_0():
    pass


@opcode(60)
def istore_1():
    pass


@opcode(61)
def istore_2():
    pass


@opcode(62)
def istore_3():
    pass


@opcode(100)
def isub():
    pass


@opcode(124)
def iushr():
    pass


@opcode(130)
def ixor():
    pass


@opcode(168, 2)
def jsr():
    pass


@opcode(201, 4)
def jsr_w():
    pass


@opcode(138)
def l2d():
    pass


@opcode(137)
def l2f():
    pass


@opcode(136)
def l2i():
    pass


@opcode(97)
def ladd():
    pass


@opcode(47)
def laload():
    pass


@opcode(127)
def land():
    pass


@opcode(80)
def lastore():
    pass


@opcode(148)
def lcmp():
    pass


@opcode(9)
def lconst_0():
    pass


@opcode(10)
def lconst_1():
    pass


@opcode(18, 1)
def ldc():
    pass


@opcode(19, 2)
def ldc_w():
    pass


@opcode(20, 2)
def ldc2_w():
    pass


@opcode(109)
def ldiv():
    pass


@opcode(22, 1)
def lload():
    pass


@opcode(30)
def lload_0():
    pass


@opcode(31)
def lload_1():
    pass


@opcode(32)
def lload_2():
    pass


@opcode(33)
def lload_3():
    pass


@opcode(105)
def lmul():
    pass


@opcode(117)
def lneg():
    pass


# TODO: Fix lookupswitch
@opcode(171)
def lookupswitch():
    pass


@opcode(129)
def lor():
    pass


@opcode(113)
def lrem():
    pass


@opcode(173)
def lreturn():
    pass


@opcode(121)
def lshl():
    pass


@opcode(123)
def lshr():
    pass


@opcode(55, 1)
def lstore():
    pass


@opcode(63)
def lstore_0():
    pass


@opcode(64)
def lstore_1():
    pass


@opcode(65)
def lstore_2():
    pass


@opcode(66)
def lstore_3():
    pass


@opcode(101)
def lsub():
    pass


@opcode(125)
def lushr():
    pass


@opcode(131)
def lxor():
    pass


@opcode(194)
def monitorenter():
    pass


@opcode(195)
def monitorexit():
    pass


@opcode(197, 3)
def multianewarray():
    pass


@opcode(187, 2)
def new():
    pass


@opcode(188, 1)
def newarray():
    pass


@opcode(0)
def nop():
    pass


@opcode(87)
def pop():
    pass


@opcode(88)
def pop2():
    pass


@opcode(181, 2)
def putfield():
    pass


@opcode(179, 2)
def putstatic():
    pass


@opcode(169, 1)
def ret():
    pass


@opcode(177)
def return_():
    pass


@opcode(53)
def saload():
    pass


@opcode(86)
def sastore():
    pass


@opcode(17, 2)
def sipush():
    pass


@opcode(95)
def swap():
    pass


# TODO: Fix tableswitch
@opcode(170)
def tableswitch():
    pass


@opcode(196, 3)
def wide():
    pass
