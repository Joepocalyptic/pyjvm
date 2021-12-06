from parser.class_parser import parse_class
import pprint


def main():
    print("Hello World w/ Fields")
    pprint.pprint(parse_class("tests/HelloWorld_Fields.class"))

    print("tableswitch")
    pprint.pprint(parse_class("tests/TableSwitch.class"))

    # print("rt.jar Class")
    # print(parse_class("tests/Class.class"))
    # print("success")


if __name__ == "__main__":
    main()
