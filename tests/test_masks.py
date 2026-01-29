import pytest

from src.masks import get_mask_account
from src.masks import get_mask_card_number


def test_mask_standard_16_digits() -> None:
    """Тестирование функции get_mask_card_number.
    Тестирование стандартного 16-значного номера карты с "int" на вводе."""
    assert get_mask_card_number(7000792289606361) == '7000 79** **** 6361'


def test_mask_fixture(fixture_card_numbers) -> None:
    """Используем фикстуру для получения данных для тестирования"""
    assert get_mask_card_number(fixture_card_numbers) == '7000 79** **** 6361'


def test_invalid_cards_fixture(fixture_invalid_card_numbers) -> None:
    """Тестирование невалидных номеров карт через фикстуру"""
    for test_case in fixture_invalid_card_numbers:
        with pytest.raises(ValueError, match=test_case["error"]):
            get_mask_card_number(test_case["number"])


def test_mask_with_spaces_input() -> None:
    """Тестирование номера с пробелами."""
    assert get_mask_card_number('7000 7922 8960 6361') == '7000 79** **** 6361'


def test_mask_with_dashes_input() -> None:
    """Тестирование номера с дефисами на входе"""
    assert get_mask_card_number('7000-7922-8960-6361') == '7000 79** **** 6361'


def test_mask_empty_string() -> None:
    """Тестирование пустой строки - должно выбрасывать исключение"""
    with pytest.raises(ValueError, match='Не корректные входные данные: номер не содержит цифр'):
        get_mask_card_number('')


def test_mask_not_16_digits() -> None:
    """Тестирование номера не содержащего 16 цифр"""
    with pytest.raises(ValueError, match='Не корректные входные данные: номер должен содержать 16 цифр'):
        get_mask_card_number('123')


@pytest.mark.parametrize('card_number, expected', [
    ('1234567890123456', '1234 56** **** 3456'),
    ('4000123456789010', '4000 12** **** 9010'),
    ('5555555555554444', '5555 55** **** 4444'),
    ('1234 5678 9012 3456', '1234 56** **** 3456'),
    ('1234-5678-9012-3456', '1234 56** **** 3456'),
    ])
def test_get_mask_card_number_parametrized(card_number, expected) -> None:
    """Параметризованный тест различных случаев"""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize('card_number, error_message', [
    (None, 'получен None'),
    ('', 'Не корректные входные данные: номер не содержит цифр'),
    ('abc', 'Не корректные входные данные: номер не содержит цифр'),
    ('123', 'Не корректные входные данные: номер должен содержать 16 цифр'),
])
def test_get_mask_card_number_errors(card_number, error_message) -> None:
    """Параметризованный тест некорректных случаев"""
    with pytest.raises(ValueError, match=error_message):
        get_mask_card_number(card_number)


def test_get_mask_account() -> None:
    """Тестирование функции get_mask_account.
    Тестирование стандартного 20-значного номера карты с "int" на вводе."""
    assert get_mask_account(73654108430135874305) == '**4305'


def test_mask_account_fixture(fixture_account_numbers) -> None:
    """Используем фикстуру для получения данных для тестирования"""
    assert get_mask_account(fixture_account_numbers) == '**4305'


def test_invalid_accounts_fixture(fixture_invalid_account_numbers) -> None:
    """Тестирование невалидных номеров счетов через фикстуру"""
    for test_case in fixture_invalid_account_numbers:
        with pytest.raises(ValueError, match=test_case["error"]):
            get_mask_account(test_case["number"])


def test_mask_account_normal() -> None:
    """Тестирование стандартного номера счета (20 цифр)."""
    assert get_mask_account("12345678901234567890") == "**7890"


@pytest.mark.parametrize('account_number, error_message', [
    (None, 'получен None'),
    ([], 'Не корректный тип данных'),
    ({}, 'Не корректный тип данных'),
    ('', 'Не корректные входные данные: номер не содержит цифр'),
    ('abc', 'Не корректные входные данные: номер не содержит цифр'),
    ('ABC-DEF-GHI-JKL', 'Не корректные входные данные: номер не содержит цифр'),
    ('   ', 'Не корректные входные данные: номер не содержит цифр'),
    ('123abc456def789', 'Не корректные входные данные: номер должен содержать только цифры'),
    ('1234 5678 9012 3456', 'Не корректные входные данные: номер должен содержать только цифры'),
    ('1234-5678-9012-3456', 'Не корректные входные данные: номер должен содержать только цифры'),
    ('123', 'Не корректные входные данные: номер должен содержать 20 цифр'),
    ('12345', 'Не корректные входные данные: номер должен содержать 20 цифр'),
    ('1234567890123456789', 'Не корректные входные данные: номер должен содержать 20 цифр'),
    ('123456789012345678901', 'Не корректные входные данные: номер должен содержать 20 цифр'),
    ('@#$%^&*()', 'Не корректные входные данные: номер не содержит цифр'),
])
def test_mask_account_invalid_input(account_number: str, error_message: str) -> None:
    """Тестирование некорректных входных данных"""
    with pytest.raises(ValueError, match=error_message):
        get_mask_account(account_number)


@pytest.mark.parametrize('account_number, expected_output', [
    # Валидные номера счетов (20 цифр)
    ('12345678901234567890', '**7890'),
    ('98765432109876543210', '**3210'),
    ('00000000000000000001', '**0001'),
    ('99999999999999999999', '**9999'),
    ('00000000123456789012', '**9012'),
])
def test_mask_account_valid_inputs(account_number: str, expected_output: str) -> None:
    """Параметризованный тест для валидных входных данных"""
    assert get_mask_account(account_number) == expected_output


def test_mask_account_whitespace_with_digits() -> None:
    """Тестирование строки с пробелами и цифрами"""
    with pytest.raises(ValueError, match='Не корректные входные данные: номер должен содержать только цифры'):
        get_mask_account('1234 5678 9012 3456 7890')
