# Функция get_mask_card_number:
# Тестирование правильности маскирования номера карты.
# Проверка работы функции на различных входных форматах номеров карт,
# включая граничные случаи и нестандартные длины номеров.
# Проверка, что функция корректно обрабатывает входные строки, где отсутствует номер карты.

# Функция get_mask_account:
# Тестирование правильности маскирования номера счета.
# Проверка работы функции с различными форматами и длинами номеров счетов.
# Проверка, что функция корректно обрабатывает входные данные, где номер счета меньше ожидаемой длины.
import pytest
from src.masks import get_mask_account
from src.masks import get_mask_card_number

def test_mask_standard_16_digits():
    """Тестирование функции get_mask_card_number.
    Тестирование стандартного 16-значного номера карты с "int" на вводе."""
    assert get_mask_card_number(7000792289606361) == '7000 79** **** 6361'


def test_mask_with_spaces_input():
    """Тестирование номера с пробелами."""
    assert get_mask_card_number('7000 7922 8960 6361') == '7000 79** **** 6361'


def test_mask_with_dashes_input():
    """Тестирование номера с дефисами на входе"""
    assert get_mask_card_number('7000-7922-8960-6361') == '7000 79** **** 6361'


def test_mask_empty_string():
    """Тестирование пустой строки - должно выбрасывать исключение"""
    with pytest.raises(ValueError, match='Не корректные входные данные: номер не содержит цифр'):
        get_mask_card_number('')


def test_mask_not_16_digits():
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
def test_get_mask_card_number_parametrized(card_number, expected):
    """Параметризованный тест различных случаев"""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize('card_number, error_message', [
    # Некорректные номера
    (None, 'получен None'),
    ('', 'Не корректные входные данные: номер не содержит цифр'),
    ('abc', 'Не корректные входные данные: номер не содержит цифр'),
    ('123', 'Не корректные входные данные: номер должен содержать 16 цифр'),
])
def test_get_mask_card_number_errors(card_number, error_message):
    """Параметризованный тест некорректных случаев"""
    with pytest.raises(ValueError, match=error_message):
        get_mask_card_number(card_number)


def test_get_mask_account():
    """Тестирование функции get_mask_account."""
    assert get_mask_account(73654108430135874305) == '**4305'

