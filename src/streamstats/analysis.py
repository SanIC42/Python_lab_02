import csv
import datetime
import json
import logging

from .errors import InvalidEventError, InvalidTimestampError, MixedAwareNaiveError

logger = logging.getLogger(__name__)
report = {}


def data_calculation(file_name: str, format: str, skip_invalid: bool) -> None:
    """Анализ файлов для отчёта"""

    res = {
        "event_count": 0,
        "levels": {"DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0},
        "sources": {},
        "top_5_sources": {},
        "first_timestamp": "",
        "last_timestamp": "",
    }

    if skip_invalid:
        res["skipped_lines"] = 0

    if format == "csv":
        with open(file=file_name, encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=",")

            next(reader)

            for line_num, line in enumerate(reader, start=1):
                try:
                    timestamp, level, source, _message = line  # _ в _message для ruff

                    # подсчёт количества событий каждого уровня
                    res["levels"][level] += 1

                    # подсчёт количества событий каждого источника
                    res["sources"][source] = res["sources"].get(source, 0) + 1

                    # Поиск первой и последней временных меток
                    timestamp = datetime.datetime.fromisoformat(timestamp)
                    # первая
                    if not res["first_timestamp"]:
                        res["first_timestamp"] = timestamp
                    else:
                        res["first_timestamp"] = min(res["first_timestamp"], timestamp)

                    # последняя
                    if not res["last_timestamp"]:
                        res["last_timestamp"] = timestamp
                    else:
                        res["last_timestamp"] = max(res["last_timestamp"], timestamp)

                    # подсчёт общего количества событий
                    res["event_count"] += 1

                except TypeError:
                    if skip_invalid:
                        res["skipped_lines"] += 1
                        logger.warning(
                            "%s:%d: Смешивание aware и naive временных меток",
                            file_name,
                            line_num,
                        )
                    else:
                        raise MixedAwareNaiveError

                except ValueError:
                    if skip_invalid:
                        res["skipped_lines"] += 1
                        logger.warning(
                            "%s:%d: Неверная временная метка", file_name, line_num
                        )
                    else:
                        raise InvalidTimestampError

                except Exception:  # noqa: BLE001
                    if skip_invalid:
                        res["skipped_lines"] += 1
                        logger.warning("%s:%d: Неверное событие", file_name, line_num)
                    else:
                        raise InvalidEventError

    elif format == "jsonl":
        with open(file=file_name, encoding="utf-8") as file:
            for line_num, line in enumerate(file, start=1):
                try:
                    data = json.loads(line)

                    timestamp, level, source, _message = (  # _ в _message для ruff
                        data["timestamp"],
                        data["level"],
                        data["source"],
                        data["message"],
                    )

                    # подсчёт количества событий каждого уровня
                    res["levels"][level] += 1

                    # подсчёт количества событий каждого источника
                    res["sources"][source] = res["sources"].get(source, 0) + 1

                    # Поиск первой и последней временных меток
                    timestamp = datetime.datetime.fromisoformat(timestamp)
                    # первая
                    if not res["first_timestamp"]:
                        res["first_timestamp"] = timestamp
                    else:
                        res["first_timestamp"] = min(res["first_timestamp"], timestamp)

                    # последняя
                    if not res["last_timestamp"]:
                        res["last_timestamp"] = timestamp
                    else:
                        res["last_timestamp"] = max(res["last_timestamp"], timestamp)

                    # подсчёт общего количества событий
                    res["event_count"] += 1

                except TypeError:
                    if skip_invalid:
                        res["skipped_lines"] += 1
                        logger.warning(
                            "%s:%d: Смешивание aware и naive временных меток",
                            file_name,
                            line_num,
                        )
                    else:
                        raise MixedAwareNaiveError

                except ValueError:
                    if skip_invalid:
                        res["skipped_lines"] += 1
                        logger.warning(
                            "%s:%d: Неверная временная метка", file_name, line_num
                        )
                    else:
                        raise InvalidTimestampError

                except Exception:  # noqa: BLE001
                    if skip_invalid:
                        res["skipped_lines"] += 1
                        logger.warning("%s:%d: Неверное событие", file_name, line_num)
                    else:
                        raise InvalidEventError

    res["top_5_sources"] = dict(
        list(sorted(res["sources"].items(), key=lambda x: -x[1])[:5])
    )
    res["first_timestamp"] = str(res["first_timestamp"])
    res["last_timestamp"] = str(res["last_timestamp"])

    report[file_name] = res
