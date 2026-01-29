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
