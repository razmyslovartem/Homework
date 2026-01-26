# Общие аспекты тестирования
# Фикстуры. Для всех тестов создайте фикстуры,
# которые предоставят тестовые данные для списков словарей,
# включая различные случаи и комбинации state и date.
#
# Покрытие тестами.
# Убедитесь, что все ветви кода и исключения,
# которые могут быть сгенерированы вашими функциями, тестируются.
from typing import Any
from typing import Dict
from typing import List

import pytest
from pytest import fixture


@fixture()
def fixture_card_numbers() -> str:
    """Фикстура для предоставления тестового номера карты"""
    return 7000792289606361

@pytest.fixture
def fixture_invalid_card_numbers() -> List[Dict[str, Any]]:
    """Фикстура с невалидными номерами карт и ожидаемыми ошибками"""
    return [
        {"number": None, "error": "Не корректные входные данные: получен None"},
        {"number": "", "error": "Не корректные входные данные: номер не содержит цифр"},
        {"number": "abc", "error": "Не корректные входные данные: номер не содержит цифр"},
        {"number": "123", "error": "Не корректные входные данные: номер должен содержать 16 цифр"},
    ]

@fixture()
def fixture_account_numbers() -> str:
    """Фикстура для предоставления тестового номера счета"""
    return 73654108430135874305


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


@pytest.mark.parametrize('word, correct', [('шалаш', True),
                                           ('привет', False),
                                           ('казак', True),
                                           ('ура', False)])
def test_is_palindrom(word, correct):
    assert is_palindrom(word) == correct


def test_error_is_palindrom():
    with pytest.raises(TypeError):
        is_palindrom(1)


