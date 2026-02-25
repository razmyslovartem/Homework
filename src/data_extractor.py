"""
В модуле data_extractor.py
В этом модуле реализованы функции считывания финансовых операций
из файлов CSV- и XLSX-файлов из data.
"""

import os

import pandas as pd
from dotenv import load_dotenv


def get_info_csv(file_path: str) -> list[dict]:
    """
    Считывает данные из CSV файла через pandas и возвращает
    список словарей (orient='records')
    """
    df = pd.read_csv(file_path, sep=";", encoding="utf-8")
    data = df.to_dict(orient="records")
    return data


def get_info_xlsx(file_path: str) -> list[dict]:
    """
    Считывает данные из XLSX файла через pandas и возвращает
    список словарей (orient='records')
    """
    df = pd.read_excel(file_path)
    data = df.to_dict(orient="records")
    return data


if __name__ == "__main__":  # pragma: no cover
    load_dotenv()  # Загрузка переменных из .env-файла.

    file_csv_path = os.getenv("FILE_PATH_CSV", "default_log_file.csv")
    file_xlsx_path = os.getenv("FILE_PATH_XLSX", "default_log_file.xlsx")

    data_csv = get_info_csv(file_csv_path)
    data_xlsx = get_info_xlsx(file_xlsx_path)

    # for transaction in data_csv:
    #     print(transaction)

    for transaction in data_xlsx:
        print(transaction)
