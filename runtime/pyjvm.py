from objects.classes import Class, ClassInstance
from objects.fields import FieldFlags
from objects.runtime import Frame
from parser.class_parser import parse_class


default_fields = {
    "B": b"0",
    "C": "\u0000",
    "D": 0.0,
    "F": 0.0,
    "I": 0,
    "J": 0,
    "L": None,
    "S": 0,
    "Z": False,
    "[": None
}


class JVM:
    method_area = list[Class]()
    stack = list[Frame]()
    heap = list[ClassInstance]()
    pc = 0

    def __init__(self, init_filename: str):
        self.init_class = self.__cycle(parse_class(init_filename))
        print(self.method_area)
        print(self.heap)

    def __load(self, clazz: Class):
        self.method_area.append(clazz)
        return clazz

    def __init(self, clazz: Class):
        fields = dict[str, any]()
        
        for field in clazz.fields:
            if FieldFlags.ACC_STATIC in field.access_flags:
                fields[field.name] = default_fields[field.descriptor[0]]

        instance = ClassInstance(
            clazz.this_class,
            fields
        )

        self.heap.append(instance)
        return instance
        
    def __cycle(self, clazz: Class):
        return self.__init(
               self.__load(clazz))