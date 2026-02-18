import json
from typing import List, Dict, Any


def read_json(json_path: str) -> List[Dict[str, Any]]:
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return [transaction for transaction in data if transaction]
        else:
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        # Если файл не найден или не является валидным JSON
        return []
    except Exception:
        # Любые другие ошибки
        return []


if __name__ == "__main__":
    json_path = '../data/operations.json'
    transactions = read_json(json_path)
    print(f"Найдено транзакций: {len(transactions)}")
