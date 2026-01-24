def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Функция принимает список словарей с банковскими операциями.
    Возвращает новый список, содержащий только те словари,
    у которых ключ 'state' соответствует указанному значению.

    Параметр operations принимает список словарей с операциями.
    Параметр state принимает значение для фильтрации (по умолчанию 'EXECUTED').
    Параметр возвращает отфильтрованный список словарей.
    """
    filtered_operations = []
    for operation in operations:
        if operation.get("state") == state:
            filtered_operations.append(operation)
    return filtered_operations


# Тестирование:
test_data = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

# Тест 1: значение по умолчанию 'EXECUTED'
result1 = filter_by_state(test_data)
print("Результат с state='EXECUTED' (по умолчанию):")
print(result1)

# Тест 2: явное указание 'CANCELED'
result2 = filter_by_state(test_data, "CANCELED")
print("\nРезультат с state='CANCELED':")
print(result2)


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]:
    """
    Функция принимает список словарей с банковскими операциями.
    Возвращает новый список, отсортированный по дате (ключ 'date').

    Параметр operations принимает список словарей с операциями.
    Параметр reverse принимает порядок сортировки (True - по убыванию, False - по возрастанию).
    Параметр return возвращает отсортированный список словарей.
    """
    # Создаем копию списка, чтобы не изменять оригинал
    sorted_operations = operations.copy()

    # Сортируем по дате
    # Даты уже в ISO формате, который можно сравнивать как строки
    sorted_operations.sort(key=lambda x: x.get("date", ""), reverse=reverse)

    return sorted_operations


test_data = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

# Тест 1: сортировка по убыванию (по умолчанию, reverse=True)
result1 = sort_by_date(test_data)
print("Сортировка по убыванию (новые сначала):")
for op in result1:
    print(f"ID: {op['id']}, Дата: {op['date']}, State: {op['state']}")

# Тест 2: сортировка по возрастанию (reverse=False)
result2 = sort_by_date(test_data, reverse=False)
print("\nСортировка по возрастанию (старые сначала):")
for op in result2:
    print(f"ID: {op['id']}, Дата: {op['date']}")
