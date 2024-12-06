import argparse
import importlib


def get_class_from_string(class_path: str):
    module_name, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def main():
    parser = argparse.ArgumentParser(description="Example script")
    parser.add_argument(
        "--formatterClass",
        type=str,
        help="The fully qualified name of the formatter class to use, e.g., 'foo.bar.MyFormatter'",
    )
    args = parser.parse_args()

    if args.formatterClass:
        FormatterClass = get_class_from_string(args.formatterClass)
        formatter_instance = FormatterClass()
        print(f"Created an instance of {FormatterClass}: {formatter_instance}")
    else:
        print("No formatter class provided.")


if __name__ == "__main__":
    main()
