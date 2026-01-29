from typing import Any
from typing import Dict
from typing import List

import pytest


@pytest.fixture()
def fixture_card_numbers() -> str:
    """Фикстура для предоставления тестового номера карты"""
    return "7000792289606361"


@pytest.fixture
def fixture_invalid_card_numbers() -> List[Dict[str, Any]]:
    """Фикстура с невалидными номерами карт и ожидаемыми ошибками"""
    return [
        {"number": None, "error": "Не корректные входные данные: получен None"},
        {"number": "", "error": "Не корректные входные данные: номер не содержит цифр"},
        {"number": "abc", "error": "Не корректные входные данные: номер не содержит цифр"},
        {"number": "123", "error": "Не корректные входные данные: номер должен содержать 16 цифр"},
    ]


@pytest.fixture()
def fixture_account_numbers() -> str:
    """Фикстура для предоставления тестового номера счета"""
    return "73654108430135874305"


@pytest.fixture
def fixture_invalid_account_numbers() -> List[Dict[str, Any]]:
    """Фикстура с невалидными номерами счетов и ожидаемыми ошибками"""
    return [
        {"number": None, "error": "получен None"},
        {"number": [], "error": "Не корректный тип данных"},
        {"number": {}, "error": "Не корректный тип данных"},
        {"number": "", "error": "Не корректные входные данные: номер не содержит цифр"},
        {"number": "abc", "error": "Не корректные входные данные: номер не содержит цифр"},
        {"number": "   ", "error": "Не корректные входные данные: номер не содержит цифр"},
        {"number": "123", "error": "Не корректные входные данные: номер должен содержать 20 цифр"},
    ]


@pytest.fixture
def valid_card_data() -> List[Dict[str, Any]]:
    """Фикстура: список словарей с валидными картами и счетами."""
    return [
        {"input": "Visa Platinum 7000792289603456", "expected": "Visa Platinum 7000 79** **** 3456"},
        {"input": "Maestro 7000792289606361", "expected": "Maestro 7000 79** **** 6361"},
        {"input": "МИР 1234567890123456", "expected": "МИР 1234 56** **** 3456"},
        {"input": "American Express 5555555555554444", "expected": "American Express 5555 55** **** 4444"},
        {"input": "Visa Classic 4000123456789010", "expected": "Visa Classic 4000 12** **** 9010"},
        {
            "input": "Счет 73654108430135874305",
            "expected": "Счет **4305",
        },
    ]


@pytest.fixture
def invalid_mask_account_card_cases() -> List[Dict[str, Any]]:
    """Фикстура с невалидными данными для mask_account_card"""
    return [
        {"input": "", "error": "Передана пустая строка"},
        {"input": "   ", "error": "Передана пустая строка"},
        {"input": "Visa", "error": "Строка должна содержать название и номер"},
        {"input": "1234567890123456", "error": "Строка должна содержать название и номер"},
        {"input": "Visa 1234", "error": "номер должен содержать 16 или 20 цифр"},
        {"input": "Visa abcdefghijklmnop", "error": "номер не содержит цифр"},
        {"input": "Visa 123456789012345", "error": "номер должен содержать 16 или 20 цифр"},  # 15 цифр
        {"input": "Visa 12345678901234567", "error": "номер содержит 17 цифр, ожидается 16 или 20"},
        {"input": "Счет 12345", "error": "номер должен содержать 16 или 20 цифр"},
        {"input": "Счет abcdefghijklmnopqrst", "error": "номер не содержит цифр"},
    ]


@pytest.fixture
def wrong_type_mask_account_card_cases() -> List[Dict[str, Any]]:
    """Фикстура с данными неправильного типа для mask_account_card"""
    return [
        {"input": None, "error": "Ожидалась строка, получен NoneType"},
        {"input": 1234567890123456, "error": "Ожидалась строка, получен int"},
        {"input": 123.45, "error": "Ожидалась строка, получен float"},
        {"input": True, "error": "Ожидалась строка, получен bool"},
        {"input": ["Visa", "1234567890123456"], "error": "Ожидалась строка, получен list"},
    ]


@pytest.fixture
def invalid_get_date_cases() -> List[Dict[str, Any]]:
    """Фикстура с невалидными данными для get_date"""
    return [
        {"input": "", "error": "Invalid isoformat string"},
        {"input": "   ", "error": "Invalid isoformat string"},
        {"input": "2024-13-11T02:26:18", "error": "month must be in 1..12"},
        {"input": "2024-03-32T02:26:18", "error": "day is out of range"},
        {"input": "2023-02-29T00:00:00", "error": "day is out of range"},
        {"input": "2024-03-11T02:26:60", "error": "second must be in 0..59"},
        {"input": "1234567890", "error": "Invalid isoformat string"},
        {"input": "2024", "error": "Invalid isoformat string"},
        {"input": "11-03-2024T02:26:18", "error": "Invalid isoformat string"},
    ]


@pytest.fixture
def test_operations_data() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми данными операций"""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 123456789, "state": "PENDING", "date": "2023-01-15T10:30:00.000000"},
    ]


@pytest.fixture
def empty_operations_data() -> List[Dict[str, Any]]:
    """Фикстура с пустым списком операций"""
    return []


@pytest.fixture
def operations_without_state():
    """Фикстура с операциями без ключа 'state'"""
    return [
        {"id": 1, "date": "2023-01-01T00:00:00.000000"},
        {"id": 2, "date": "2023-01-02T00:00:00.000000"},
    ]


@pytest.fixture
def operations_with_missing_dates(test_operations_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фикстура предоставляет операции с отсутствующими датами на основе test_operations_data"""
    modified_data = test_operations_data.copy()
    # Удаляем дату у второй операции
    modified_data[1] = modified_data[1].copy()
    del modified_data[1]["date"]
    # Удаляем дату у четвертой операции
    modified_data[3] = modified_data[3].copy()
    del modified_data[3]["date"]
    return modified_data


@pytest.fixture
def operations_with_invalid_dates(
    test_operations_data: List[Dict[str, Any]],
    invalid_get_date_cases: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Фикстура предоставляет операции с некорректными датами на основе test_operations_data"""
    modified_data = test_operations_data.copy()
    # Заменяем даты на невалидные из invalid_get_date_cases
    invalid_dates = [case["input"] for case in invalid_get_date_cases[:3]]  # Берем первые 3 невалидных даты

    for i in range(min(3, len(modified_data))):
        modified_data[i] = modified_data[i].copy()
        modified_data[i]["date"] = invalid_dates[i]

    return modified_data


@pytest.fixture
def single_operation(test_operations_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фикстура предоставляет список с одной операцией на основе test_operations_data"""
    return [test_operations_data[0].copy()]
