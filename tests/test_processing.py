# Функция sort_by_date:
# Тестирование сортировки списка словарей по датам в порядке убывания и возрастания.
# Проверка корректности сортировки при одинаковых датах.
# Тесты на работу функции с некорректными или нестандартными форматами дат.
import pytest

from src.processing import filter_by_state
# from src.processing import sort_by_date

def test_filter_by_state_default_executed(test_operations_data):
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


def test_filter_by_state_canceled(test_operations_data):
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


def test_filter_by_state_no_matching_state(test_operations_data):
    """Тест фильтрации при отсутствии операций с указанным статусом"""
    result = filter_by_state(test_operations_data, "NONEXISTENT")

    # Должен вернуться пустой список
    assert result == []
    assert len(result) == 0


def test_filter_by_state_empty_list(empty_operations_data):
    """Тест фильтрации с пустым списком операций"""
    result = filter_by_state(empty_operations_data, "EXECUTED")

    # Должен вернуться пустой список
    assert result == []
    assert len(result) == 0


def test_filter_by_state_operations_without_state(operations_without_state):
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
def test_filter_by_state_parametrized(test_operations_data, state, expected_count):
    """Параметризованный тест для различных значений state"""
    result = filter_by_state(test_operations_data, state)

    # Проверяем количество найденных операций
    assert len(result) == expected_count

    # Проверяем, что все операции имеют указанное состояние
    if expected_count > 0:
        assert all(op["state"] == state for op in result)