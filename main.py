from runtime.pyjvm import JVM


def main():
    JVM("tests/HelloWorld_Fields.class")


if __name__ == "__main__":
    main()
