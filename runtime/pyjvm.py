from objects.classes import Class
from objects.runtime import Frame
from parser.class_parser import parse_class


class JVM:
    stack = list[Frame]()
    heap = list[Class]()
    pc = 0

    def __init__(self, init_filename):
        self.init_class = parse_class(init_filename)

    def __load(self):
        pass

    def __link(self):
        pass

    def __init(self):
        pass
