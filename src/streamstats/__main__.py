import argparse
import logging
import sys

from .analysis import data_calculation, report
from .errors import (
    InputNotFoundError,
    InvalidEventError,
    InvalidInputsError,
    InvalidTimestampError,
    MixedAwareNaiveError,
    OutputAlreadyExistError,
    UnknownFieldError,
    UnsupportedFormatError,
)
from .parsers import CLI_validation, files_validation
from .report import make_report


def main():
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )

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
        help="путь к json-файлу отчёта",
    )
    analyze.add_argument(
        "--skip-invalid",
        dest="skip_invalid",
        action="store_true",
        help="пропускать некорректные записи вместо остановки с ошибкой",
    )

    args = parser.parse_args()

    try:
        # валидация ввода пользователя
        CLI_validation(args.inputs, args.format, args.output)

        # валидация файлов
        for file in args.inputs:
            files_validation(file, args.format, args.skip_invalid)

        # анализ файлов для отчёта
        for file in args.inputs:
            data_calculation(file, args.format, args.skip_invalid)

        # формирование отчёта
        make_report(report, args.output)

    except InputNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(2)

    except OutputAlreadyExistError as e:
        print(e, file=sys.stderr)
        sys.exit(2)

    except InvalidInputsError as e:
        print(e, file=sys.stderr)
        sys.exit(2)

    except UnsupportedFormatError as e:
        print(e, file=sys.stderr)
        sys.exit(2)

    except UnknownFieldError as e:
        print(e, file=sys.stderr)
        sys.exit(2)

    except InvalidEventError as e:
        print(e, file=sys.stderr)
        sys.exit(2)

    except InvalidTimestampError as e:
        print(e, file=sys.stderr)
        sys.exit(2)

    except MixedAwareNaiveError as e:
        print(e, file=sys.stderr)
        sys.exit(2)

    except Exception as e:  # noqa: BLE001
        print(e, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
