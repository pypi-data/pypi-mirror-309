# mytool.py
import argparse

def main():
    parser = argparse.ArgumentParser(description="Prismio", usage="Prismio <command> [options]")
    parser.add_argument('--version', action='store_true', help='Show version')
    args = parser.parse_args()
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    greet_parser = subparsers.add_parser("greet", help="Greet a user by name")
    greet_parser.add_argument("test", type=str, help="IDK")

    if args.command == "greet":
        print(args.test)
    if args.version:
        print("MyTool version 1.0")

if __name__ == "__main__":
    main()
