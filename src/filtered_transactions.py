from collections import Counter
import os
import re

from dotenv import load_dotenv

from src.data_extractor import get_info_csv


def process_bank_search(data: list[dict], search_text: str) -> list[dict]:
    """Фильтрация трансакции по ключевому слову"""
    pattern = re.compile(search_text, flags=re.IGNORECASE)
    result = []
    for transaction in data:
        if pattern.search(str(transaction["description"])):
            result.append(transaction)
        else:
            continue

    return result


def process_bank_operations(data: list[dict], categories: list[str]) -> dict[str, int]:
    """Фильтрация трансакции по категориям с подсчётом операций в категориях"""
    filter_categories = []

    for transaction in data:
        category = transaction.get("description")

        if category not in categories:
            continue
        else:
            filter_categories.append(category)

    result = Counter(filter_categories)
    return dict(result)


if __name__ == "__main__":  # pragma: no cover
    load_dotenv()  # Загрузка переменных из .env-файла.
    file_csv_path = os.getenv("FILE_PATH_CSV", "default_log_file.csv")

    data = get_info_csv(file_csv_path)
    search_text = "Перевод с карты на карту"
    categories = ["Перевод организации", "Перевод с карты на карту", "Перевод со счета на счет"]

    filter_data_1 = process_bank_search(data, search_text)
    filter_data_2 = process_bank_operations(data, categories)

    # Для 1ой функции поиск выбора.
    # for transaction in filter_data_1:
    #     print(transaction)

    # Для 2ой функции подсчёта категорий.
    for key, value in filter_data_2.items():
        print(key, value)
