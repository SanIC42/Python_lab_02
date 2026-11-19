class StreamStatsError(Exception):
    """Базовая ошибка пакета"""


class UnsupportedFormatError(StreamStatsError):
    """Неподдерживаемый формат входного файла"""


class InvalidEventError(StreamStatsError):
    """Неверное событие (некорректное количество полей, неверные данные столбца)"""


class InvalidTimestampError(StreamStatsError):
    """Неверная временная метка"""


class UnknownFieldError(StreamStatsError):
    """Неизвестное поле"""


class MixedAwareNaiveError(StreamStatsError):
    """Смешивание aware и naive временных меток (aware - с тайм зоной, naive - без неё)"""


class InputNotFoundError(StreamStatsError):
    """Входной файл не найден"""


class OutputAlreadyExistError(StreamStatsError):
    """Выхрдной файл уже сущействует"""


class InvalidInputsError(StreamStatsError):
    """Форматы файлов и --format отличаются"""
