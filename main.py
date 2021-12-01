import pprint

from class_parser import parse


def main():
    pprint.pprint(parse("Main.class"))


if __name__ == "__main__":
    main()
