import pytest

from src.widget import get_date
from src.widget import mask_account_card


@pytest.mark.parametrize(
    "pay_info, expected",
    [
        ("Visa Platinum 7000792289603456", "Visa Platinum 7000 79** **** 3456"),
        ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
        ("Maestro 1234567890123456", "Maestro 1234 56** **** 3456"),
        ("American Express 5555555555554444", "American Express 5555 55** **** 4444"),
        ("Visa Classic 4000123456789010", "Visa Classic 4000 12** **** 9010"),
    ],
)
def test_mask_account_card(pay_info, expected) -> None:
    """Параметризованный тест различных случаев"""
    assert mask_account_card(pay_info) == expected


def test_mask_account_card_valid_cards(valid_card_data) -> None:
    """Тест валидных карт и счетов из фикстуры (список словарей)."""
    # Аргумент valid_card_data - это фикстура из conftest.py
    # Она возвращает список словарей с тестовыми данными
    for case in valid_card_data:
        # Для каждого тестового случая из списка
        result = mask_account_card(case["input"])
        # Проверяем, что результат совпадает с ожидаемым
        assert result == case["expected"]


def test_invalid_mask_account_card(invalid_mask_account_card_cases) -> None:
    """Тестирование невалидных данных для mask_account_card"""
    for test_case in invalid_mask_account_card_cases:
        with pytest.raises(ValueError, match=test_case["error"]):
            mask_account_card(test_case["input"])


def test_wrong_type_mask_account_card(wrong_type_mask_account_card_cases) -> None:
    """Тестирование данных неправильного типа для mask_account_card"""
    for test_case in wrong_type_mask_account_card_cases:
        with pytest.raises(TypeError, match=test_case["error"]):
            mask_account_card(test_case["input"])


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024-12-31T23:59:59.999999", "31.12.2024"),
        ("2024-01-01T00:00:00", "01.01.2024"),
        ("2024-02-29T14:30:00", "29.02.2024"),
        ("2023-06-15T12:00:00.123", "15.06.2023"),
    ],
)
def test_get_date_parametrized(input_str, expected) -> None:
    """Параметризованный тест для разных дат-времени"""
    result = get_date(input_str)
    assert result == expected


@pytest.mark.parametrize(
    "wrong_input, error_type",
    [
        ("2024-13-01T00:00:00", ValueError),  # месяц 13
        ("2024-12-32T00:00:00", ValueError),  # день 32
        ("not-a-datetime", ValueError),  # не дата
        ("", ValueError),  # пустая строка
    ],
)
def test_bad_inputs_parametrized_with_type(wrong_input, error_type):
    """Параметризованный тест с указанием типа ошибки"""
    with pytest.raises(error_type):
        get_date(wrong_input)


def test_invalid_datetime_simple():
    """Упрощенная проверка невалидных дат-времени"""
    invalid_cases = [
        "2024-13-11T02:26:18",  # несуществующий месяц
        "2024-03-32T02:26:18",  # несуществующий день
        "11.03.2024T02:26:18",  # обратный формат даты
        "2024-03-11T25:26:18",  # неверный час
        "not-a-date",  # вообще не дата
    ]

    for invalid_str in invalid_cases:
        with pytest.raises(ValueError):
            get_date(invalid_str)


def test_using_fixture_simple(invalid_get_date_cases):
    """Тест с использованием фикстуры (проверяем только что есть ошибка)"""
    for test_case in invalid_get_date_cases:
        with pytest.raises(ValueError):
            get_date(test_case["input"])
