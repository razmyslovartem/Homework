# Общие аспекты тестирования
# Фикстуры. Для всех тестов создайте фикстуры,
# которые предоставят тестовые данные для списков словарей,
# включая различные случаи и комбинации state и date.
#
# Покрытие тестами.
# Убедитесь, что все ветви кода и исключения,
# которые могут быть сгенерированы вашими функциями, тестируются.

import pytest
from pytest import fixture


@fixture()
def numbers():
    return [1, 2, 3, 4]

@fixture()
def card_numbers():
    return 7000792289606361


@fixture()
def account_numbers():
    return 73654108430135874305


@pytest.mark.parametrize('word, correct', [('шалаш', True),
                                           ('привет', False),
                                           ('казак', True),
                                           ('ура', False)])
def test_is_palindrom(word, correct):
    assert is_palindrom(word) == correct


def test_error_is_palindrom():
    with pytest.raises(TypeError):
        is_palindrom(1)


