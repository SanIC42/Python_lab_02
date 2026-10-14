# Лабораторная работа 2. Потоковый анализатор файлов


## Краткое Описание

Пакет `streamstats`, читающий события из CSV и JSONL и создающий статистический отчёт.


## Структура

<pre>
lab_02/
  pyproject.toml
  README.md
  src/streamstats/
    __init__.py
    __main__.py
    analysis.py
    errors.py
    models.py
    parsers.py
    report.py
  tests/
</pre>


## Первая настройка

Выполнить в консоли:
```powershell
pip install -e .
```


## Команды

Справка:
```powershell
python -m streamstats --help
```


```powershell
python -m streamstats analyze INPUT [INPUT ...] --format csv|jsonl --output REPORT.json
```


```powershell
python -m streamstats analyze INPUT --format jsonl --skip-invalid
```
