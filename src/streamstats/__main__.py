import argparse
import sys


def main():
    parser = argparse.ArgumentParser(prog="python -m streamstats")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser(
        "analyze",
        help="потоковый анализатор файлов",
    )

    analyze.add_argument(
        "inputs",
        metavar="INPUT",  # подсказка в терминале
        nargs="+",  # для ввода нескольких аргументов
        help="путь к входному файлу (можно указать несколько)",
    )
    analyze.add_argument(
        "--format",
        choices=["csv", "jsonl"],
        required=True,
        help="формат входных файлов",
    )
    analyze.add_argument(
        "--output",
        metavar="REPORT.json",  # подсказка в терминале
        help="путь к файлу отчёта (если не указан, отчёт выводится в stdout)",
    )
    analyze.add_argument(
        "--skip-invalid",
        action="store_true",
        help="пропускать некорректные записи вместо остановки с ошибкой",
    )

    args = parser.parse_args()

    if args.command == "analyze":
        pass


if __name__ == "__main__":
    sys.exit(main())
