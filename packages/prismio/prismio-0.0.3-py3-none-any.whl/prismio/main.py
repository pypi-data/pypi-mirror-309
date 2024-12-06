# mytool.py
import argparse

def main():
    parser = argparse.ArgumentParser(description="My custom CLI tool")
    parser.add_argument('--version', action='store_true', help='Show version')
    args = parser.parse_args()

    if args.version:
        print("MyTool version 1.0")

if __name__ == "__main__":
    main()
