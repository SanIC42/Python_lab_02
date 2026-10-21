class StreamStatsError(Exception):
    pass

class UnsupportedFormat(StreamStatsError):
    pass

class WrongEvent(StreamStatsError):
    pass

class WrongTimeStamp(StreamStatsError):
    pass

class CLIconfError(StreamStatsError):
    pass