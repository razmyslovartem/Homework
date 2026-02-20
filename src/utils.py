import json
import logging
import os
from typing import Any
from typing import Dict
from typing import List

# Переменные для формирования точного пути до лог-файла.
path_inside_project = os.path.dirname(os.path.abspath(__file__))
path_inside_logs = "../logs/utils.log"

# Создаем путь до файла логов относительно текущей директории.
full_path = os.path.join(path_inside_project, path_inside_logs)
abs_path = os.path.abspath(full_path)


logger = logging.getLogger("utils")  # pragma: no cover
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(filename=abs_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_json(json_path: str) -> List[Dict[str, Any]]:
    """Функция, которая принимает на вход путь до JSON-файла и возвращает список транзакций"""
    logger.info(f"Функция приняла адрес до лог-файла трансакций: {json_path}")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.debug("Данные из указанного файла считаны корректно")
        if isinstance(data, list):
            return [transaction for transaction in data if transaction]
        else:
            logger.warning("Данные пустые, функция выдала пустой список данных")
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        # Если файл не найден или не является валидным JSON
        logger.error("Файл не найден или не является валидным JSON")
        return []
    except Exception:
        # Любые другие ошибки
        return []


if __name__ == "__main__":
    json_path = "../data/operations.json"
    transactions = read_json(json_path)
    print(f"Найдено транзакций: {len(transactions)}")
