import csv
import json
import os
from datetime import datetime

from .errors import (
    InputNotFoundError,
    InvalidEventError,
    InvalidInputsError,
    InvalidTimestampError,
    OutputAlreadyExistError,
    UnsupportedFormatError,
)


def CLI_validation(inputs: list[str], format: str, output: str) -> None:
    """проверка аргументов строки на валидность"""

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
    if any(file[file.rfind(".") + 1:] != format for file in inputs):
        raise InvalidInputsError


def files_validation(file_name: str, file_type: str, skip_invalid: bool) -> None:
    """Проверка файла на корректность"""

    if file_type == "csv":
        with open(file=file_name, encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=",")

            # Пропускаем заголовок
            next(reader)

            for line in reader:
                # Ошибка 1. Неверное событие
                if len(line) != 4:
                    raise InvalidEventError

                timestamp, level, source, message = line

                # Ошибка 2. Неверная временная метка
                try:
                    if not datetime.fromisoformat(timestamp):
                        raise InvalidTimestampError
                except ValueError:
                    raise InvalidTimestampError

    elif file_type == "jsonl":
        with open(file=file_name, encoding="utf-8") as file:
            for line in file:
                try:

                    try:
                        data = json.loads(line)
                        timestamp, level, source, message = (
                            data.get("timestamp", 0),
                            data.get("level", 0),
                            data.get("source", 0),
                            data.get("message", 0),
                        )
                    
                    # Ошибка 1. Неверное событие
                    except json.decoder.JSONDecodeError:
                        raise InvalidEventError

                    # Ошибка 1. Неверное событие
                    if (
                        len(data) != 4
                        or (not timestamp)
                        or (not level)
                        or (not source)
                        or (not message)
                    ):
                        raise InvalidEventError

                    # Ошибка 2. Неверная временная метка
                    try:
                        if not datetime.fromisoformat(timestamp):
                            raise InvalidTimestampError
                    except ValueError:
                        raise InvalidTimestampError

                # Пропуск при наличии флага --skip-invalid
                except (InvalidEventError, InvalidTimestampError):
                    if skip_invalid:
                        pass


    # Ошибка 3. Неверный формат входного файла
    else:
        raise UnsupportedFormatError
