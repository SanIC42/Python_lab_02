class StreamStatsError(Exception):
    """Базовая ошибка пакета"""


class UnsupportedFormatError(StreamStatsError):
    """Неподдерживаемый формат входного файла"""


class InvalidEventError(StreamStatsError):
    """Неверное событие: не хватает поля, неверный уровень, битый JSON и т. п."""


class InvalidTimestampError(StreamStatsError):
    """Неверная временная метка."""


class CLIConfigError(StreamStatsError):
    """Ошибка конфигурации CLI (например, выходной файл уже существует)."""