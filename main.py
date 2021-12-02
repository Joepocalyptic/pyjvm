import pprint

from class_parser import parse
from opcodes import *


def main():
    # print("Hello World w/ Fields")
    # parse("HelloWorld_Fields.class")

    print("TableSwitch")
    parse("TableSwitch.class")
    # pprint.pprint(parse("TableSwitch.class"))


if __name__ == "__main__":
    main()
