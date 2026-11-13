import csv
import json
from datetime import datetime

from errors import InvalidEventError, InvalidTimestampError, UnsupportedFormatError


def validation(file_name: str) -> None:
    """Проверка файла на корректность"""

    try:
        if file_name[-3:-1] + file_name[-1] == "csv":
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

        elif file_name[-5:-1] + file_name[-1] == "jsonl":
            with open(file=file_name, encoding="utf-8") as file:
                for line in file:
                    data = json.loads(line)
                    timestamp, level, source, message = (
                        data.get("timestamp", 0),
                        data.get("level", 0),
                        data.get("source", 0),
                        data.get("message", 0),
                    )

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

        # Ошибка 3. Неверный формат входного файла
        else:
            raise (UnsupportedFormatError)
    except FileNotFoundError:
        raise (FileNotFoundError)


validation("data/test1.jsonl")
