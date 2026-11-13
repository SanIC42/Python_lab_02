class StreamStatsError(Exception):
    """Базовая ошибка пакета"""


class UnsupportedFormatError(StreamStatsError):
    """Неподдерживаемый формат входного файла"""


class InvalidEventError(StreamStatsError):
    """Неверное событие (некорректное количество полей, неверные данные столбца)"""


class InvalidTimestampError(StreamStatsError):
    """Неверная временная метка"""


class CLIConfigError(StreamStatsError):
    """Ошибка конфигурации CLI (выходной файл уже существует, входной файл не найден)"""
