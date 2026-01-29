import pytest

from src.processing import filter_by_state
from src.processing import sort_by_date

def test_filter_by_state_default_executed(test_operations_data) -> None:
    """Тест фильтрации со значением state по умолчанию (EXECUTED)"""
    result = filter_by_state(test_operations_data)

    # Проверяем, что все возвращенные операции имеют состояние EXECUTED
    assert all(op["state"] == "EXECUTED" for op in result)

    # Проверяем количество найденных операций
    assert len(result) == 2

    # Проверяем ID найденных операций
    result_ids = [op["id"] for op in result]
    assert 41428829 in result_ids
    assert 939719570 in result_ids
    assert 594226727 not in result_ids  # CANCELED не должен быть в результате


def test_filter_by_state_canceled(test_operations_data) -> None:
    """Тест фильтрации с явным указанием state='CANCELED'"""
    result = filter_by_state(test_operations_data, "CANCELED")

    # Проверяем, что все возвращенные операции имеют состояние CANCELED
    assert all(op["state"] == "CANCELED" for op in result)

    # Проверяем количество найденных операций
    assert len(result) == 2

    # Проверяем ID найденных операций
    result_ids = [op["id"] for op in result]
    assert 594226727 in result_ids
    assert 615064591 in result_ids


def test_filter_by_state_no_matching_state(test_operations_data) -> None:
    """Тест фильтрации при отсутствии операций с указанным статусом"""
    result = filter_by_state(test_operations_data, "NONEXISTENT")

    # Должен вернуться пустой список
    assert result == []
    assert len(result) == 0


def test_filter_by_state_empty_list(empty_operations_data) -> None:
    """Тест фильтрации с пустым списком операций"""
    result = filter_by_state(empty_operations_data, "EXECUTED")

    # Должен вернуться пустой список
    assert result == []
    assert len(result) == 0


def test_filter_by_state_operations_without_state(operations_without_state) -> None:
    """Тест фильтрации операций без ключа 'state'"""
    result = filter_by_state(operations_without_state, "EXECUTED")

    # Должен вернуться пустой список, так как нет операций с ключом 'state'
    assert result == []
    assert len(result) == 0


@pytest.mark.parametrize("state, expected_count", [
    ("EXECUTED", 2),
    ("CANCELED", 2),
    ("PENDING", 1),
    ("FAILED", 0),
    ("COMPLETED", 0),
])
def test_filter_by_state_parametrized(test_operations_data, state, expected_count) -> None:
    """Параметризованный тест для различных значений state"""
    result = filter_by_state(test_operations_data, state)

    # Проверяем количество найденных операций
    assert len(result) == expected_count

    # Проверяем, что все операции имеют указанное состояние
    if expected_count > 0:
        assert all(op["state"] == state for op in result)


def test_sort_by_date_descending(test_operations_data) -> None:
    """Тест сортировки по убыванию даты (новые операции первыми)."""
    result = sort_by_date(test_operations_data, reverse=True)

    # Проверяем порядок операций (от новых к старым)
    dates = [op.get("date", "") for op in result]
    sorted_dates_desc = sorted(dates, reverse=True)

    assert dates == sorted_dates_desc
    assert result[0]["id"] == 123456789
    assert result[-1]["id"] in [939719570, 594226727, 615064591]


def test_sort_by_date_ascending(test_operations_data):
    """Тест сортировки по возрастанию даты (старые операции первыми)."""
    result = sort_by_date(test_operations_data, reverse=False)

    # Проверяем порядок операций (от старых к новым)
    dates = [op.get("date", "") for op in result]
    sorted_dates_asc = sorted(dates, reverse=False)

    assert dates == sorted_dates_asc
    assert result[0]["date"] == "2018-06-30T02:08:58.425572"
    assert result[-1]["id"] == 123456789


def test_sort_with_missing_dates(operations_with_missing_dates):
    """Тест сортировки при отсутствующих датах в некоторых операциях."""
    result = sort_by_date(operations_with_missing_dates, reverse=True)

    # Операции без дат должны быть в конце при сортировке по убыванию
    # Находим операции без дат в исходных данных
    missing_date_ids = []
    for op in operations_with_missing_dates:
        if "date" not in op:
            missing_date_ids.append(op["id"])

    # Проверяем, что операции без дат в конце результата
    result_ids = [op["id"] for op in result]
    for missing_id in missing_date_ids:
        assert missing_id in result_ids
        # Проверяем, что они действительно в конце
        position = result_ids.index(missing_id)
        assert position >= len(result_ids) - len(missing_date_ids)


def test_sort_with_invalid_dates(operations_with_invalid_dates):
    """Тест сортировки с некорректными форматами дат."""
    result = sort_by_date(operations_with_invalid_dates, reverse=True)

    # Проверяем, что функция не падает при невалидных датах
    assert len(result) == len(operations_with_invalid_dates)

    # Собираем все даты из результата
    result_dates = [op.get("date", "") for op in result]

    # Проверяем, что сортировка выполнена (по алфавиту строк)
    # При reverse=True невалидные даты типа "" и "   " будут в конце
    for i in range(len(result_dates) - 1):
        # Для строк: пустая строка считается "меньшей"
        if result_dates[i] and result_dates[i + 1]:
            # Проверяем, что сортировка по убыванию работает для непустых строк
            assert result_dates[i] >= result_dates[i + 1]


def test_sort_empty_list(empty_operations_data):
    """Тест сортировки пустого списка."""
    result = sort_by_date(empty_operations_data, reverse=True)

    assert result == []
    assert len(result) == 0


def test_sort_single_operation(single_operation):
    """Тест сортировки списка с одной операцией."""
    result = sort_by_date(single_operation, reverse=True)

    assert result == single_operation
    assert len(result) == 1
    assert result[0]["id"] == 41428829


def test_sort_mixed_valid_invalid_dates(operations_with_invalid_dates, test_operations_data):
    """Тест сортировки списка со смешанными валидными и невалидными датами."""
    # Смешиваем валидные и невалидные данные
    mixed_data = test_operations_data[:2] + operations_with_invalid_dates[:2]

    result = sort_by_date(mixed_data, reverse=True)

    # Проверяем, что функция не падает
    assert len(result) == len(mixed_data)

    # Проверяем, что все элементы присутствуют
    result_ids = {op["id"] for op in result}
    mixed_ids = {op["id"] for op in mixed_data}
    assert result_ids == mixed_ids


def test_sort_with_special_date_formats(test_operations_data):
    """Тест сортировки с разными форматами дат."""
    modified_data = test_operations_data.copy()

    # Добавляем операцию с датой без микросекунд
    new_op = {"id": 999999999, "state": "EXECUTED", "date": "2024-01-01T00:00:00"}
    modified_data.append(new_op)

    result = sort_by_date(modified_data, reverse=True)

    # Проверяем, что новая операция с датой 2024 года в начале
    assert result[0]["id"] == 999999999
    # Проверяем, что сортировка выполнена
    dates = [op.get("date", "") for op in result]
    assert dates == sorted(dates, reverse=True)
