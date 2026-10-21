import argparse
import sys


def main():
    parser = argparse.ArgumentParser(prog="python -m streamstats")
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Доступные команды",
    )
    args = parser.parse_args()


if __name__ == "__main__":
    main()
