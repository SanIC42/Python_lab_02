import json


def make_report(content: dict, output: str) -> None:
    """Запись отчёта в выходной файл"""

    # ensure_ascii сохраняет кириллицу
    # indent=4 добавляет отступы
    if output:
        with open(file=output, mode="w", encoding="utf-8") as file:
            json.dump(content, file, ensure_ascii=False, indent=4)

    else:
        with open(file="REPORT.json", mode="w", encoding="utf-8") as file:
            json.dump(content, file, ensure_ascii=False, indent=4)
