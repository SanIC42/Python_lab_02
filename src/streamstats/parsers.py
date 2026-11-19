import csv
import datetime
import json
import os

from .errors import (
    InputNotFoundError,
    InvalidEventError,
    InvalidInputsError,
    InvalidTimestampError,
    OutputAlreadyExistError,
    UnknownFieldError,
    UnsupportedFormatError,
)


def CLI_validation(inputs: list[str], format: str, output: str) -> None:
    """Проверка аргументов строки на валидность"""

    # Ошибка 1. Неподдерживаемый формат
    if format not in ["csv", "jsonl"]:
        raise UnsupportedFormatError

    # Ошибка 2. Входной файл не найден
    for file in inputs:
        if not os.path.isfile(file):
            raise InputNotFoundError

    # Ошибка 3. Выходной файл уже существует
    if (output and os.path.isfile(output)) or (
        (not output) and os.path.isfile("data/REPORT.json")
    ):
        raise OutputAlreadyExistError

    # Ошибка 4. Форматы файлов и --format отличаются
    if any(file[file.rfind(".") + 1 :] != format for file in inputs):
        raise InvalidInputsError


def files_validation(file_name: str, file_type: str, skip_invalid: bool) -> None:
    """Проверка файла на корректность"""

    if file_type == "csv":
        # пропуск при наличии флага --skip-invalid
        if skip_invalid:
            return

        with open(file=file_name, encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=",")

            # Пропускаем заголовок
            next(reader)

            for line in reader:
                # Ошибка 1. Неверное событие
                if len(line) < 4:
                    raise InvalidEventError

                # Ошибка 2. Неизвестное поле
                if len(line) > 4:
                    raise UnknownFieldError

                timestamp, level, source, message = line

                # Ошибка 3. Неверная временная метка
                try:
                    if not datetime.datetime.fromisoformat(timestamp):
                        raise InvalidTimestampError
                except ValueError:
                    raise InvalidTimestampError

    elif file_type == "jsonl":
        # пропуск при наличии флага --skip-invalid
        if skip_invalid:
            return

        with open(file=file_name, encoding="utf-8") as file:
            for line in file:
                try:
                    data = json.loads(line)
                    timestamp, level, source, message = (
                        data["timestamp"],
                        data["level"],
                        data["source"],
                        data["message"],
                    )

                    # Ошибка 1. Неверное событие
                    if (
                        len(data) < 4
                        or (not timestamp)
                        or (not level)
                        or (not source)
                        or (not message)
                    ):
                        raise InvalidEventError

                    # Ошибка 2. Неизвестное поле
                    if len(data) > 4:
                        raise UnknownFieldError

                # Ошибка 1. Неверное событие
                except json.decoder.JSONDecodeError:
                    raise InvalidEventError

                # Ошибка 3. Неверная временная метка
                try:
                    if not datetime.datetime.fromisoformat(timestamp):
                        raise InvalidTimestampError
                except ValueError:
                    raise InvalidTimestampError

    # Ошибка 4. Неверный формат входного файла
    else:
        raise UnsupportedFormatError
