from parser.class_parser import parse_class


def main():
    print("Hello World w/ Fields")
    print(parse_class("tests/HelloWorld_Fields.class"))

    print("tableswitch")
    print(parse_class("tests/TableSwitch.class"))


if __name__ == "__main__":
    main()
