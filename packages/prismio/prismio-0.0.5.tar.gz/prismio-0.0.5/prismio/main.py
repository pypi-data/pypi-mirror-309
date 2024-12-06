# mytool.py
import argparse

def greet(name):
    print(f"Hello, {name}!")

def main():
    parser = argparse.ArgumentParser(
        description="MyTool: A custom CLI tool with multiple commands",
        usage="mytool <command> [options]"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add a "greet" command
    greet_parser = subparsers.add_parser("greet", help="Greet a user by name")
    greet_parser.add_argument("name", type=str, help="The name of the person to greet")

    # Add a "version" command
    version_parser = subparsers.add_parser("version", help="Show the version of MyTool")

    # Parse the command-line arguments
    args = parser.parse_args()

    if args.command == "greet":
        greet(args.name)
    elif args.command == "version":
        print("MyTool version 1.0")
    else:
        parser.print_help()  # Show help if no command is provided

if __name__ == "__main__":
    main()
