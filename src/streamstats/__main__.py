import argparse
import sys

from .errors import (
    InputNotFoundError,
    InvalidEventError,
    InvalidInputsError,
    InvalidTimestampError,
    OutputAlreadyExistError,
    UnsupportedFormatError,
)
from .parsers import CLI_validation, files_validation


def main():
    parser = argparse.ArgumentParser(prog="python -m streamstats")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser(
        "analyze",
        help="потоковый анализатор файлов",
    )

    analyze.add_argument(
        "inputs",
        # подсказка в терминале
        metavar="INPUT",
        # для ввода нескольких аргументов
        nargs="+",
        help="путь к входному файлу (можно указать несколько)",
    )
    analyze.add_argument(
        "--format",
        dest="format",
        type=str,
        choices=["csv", "jsonl"],
        required=True,
        help="формат входных файлов",
    )
    analyze.add_argument(
        "--output",
        dest="output",
        type=str,
        # подсказка в терминале
        metavar="REPORT.json",
        help="путь к файлу отчёта",
    )
    analyze.add_argument(
        "--skip-invalid",
        dest="skip_invalid",
        action="store_true",
        help="пропускать некорректные записи вместо остановки с ошибкой",
    )

    args = parser.parse_args()

    try:
        CLI_validation(args.inputs, args.format, args.output)
        print(args.inputs)
        for file in args.inputs:
            files_validation(file, args.format, args.skip_invalid)
            print(file)

    except InputNotFoundError:
        print("Входной файл не найден")
        sys.exit(2)

    except OutputAlreadyExistError:
        print("Выходной файл уже существует")
        sys.exit(2)

    except InvalidInputsError:
        print("Форматы файлов и --format отличаются")
        sys.exit(2)

    except UnsupportedFormatError:
        print("Неподдерживаемый формат файла")
        sys.exit(2)

    except InvalidEventError:
        print("Неверное событие")
        sys.exit(2)

    except InvalidTimestampError:
        print("Неверная временная метка")
        sys.exit(2)


if __name__ == "__main__":
    main()
