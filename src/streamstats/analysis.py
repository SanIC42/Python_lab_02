def data_calculation(file_name: str):
    res = {
        "event_count": 0,
        "levels": {"DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0},
        "sources": {},
        "top_5_sources": [],
        "first_timestamp": "",
        "max_timestamp": "",
    }
