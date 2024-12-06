# mytool.py
import argparse
import rednerer
from colorama import Style, Fore, Back
import keyboard

def greet(name):
    print(f"Hello, {name}!")

def main():
    parser = argparse.ArgumentParser(
        description="Prismio: A custom CLI tool with multiple commands",
        usage="prismio <command> [options]"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add a "greet" command
    greet_parser = subparsers.add_parser("greet", help="Greet a user by name")
    greet_parser.add_argument("name", type=str, help="The name of the person to greet")

    render_parser = subparsers.add_parser("render", help="Render a video With blur-amount")
    render_parser.add_argument("filename", type=str, help="The file / vid path it has to be in your cd")
    render_parser.add_argument("amount", type=int, help="Amount recommended 1 to 8")


    # Add a "version" command
    version_parser = subparsers.add_parser("version", help="Show the version of MyTool")

    # Parse the command-line arguments
    args = parser.parse_args()

    if args.command == "greet":
        greet(args.name)
    elif args.command == "render":
        print(Fore.GREEN + "trying to Render" + Style.RESET_ALL)
        rednerer.render(args.filename, args.amount)
        print("file rendered")
    elif args.command == "version":
        print("MyTool version 1.0")
    else:
        parser.print_help()  # Show help if no command is provided

if __name__ == "__main__":
    main()
