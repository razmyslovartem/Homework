"""
Тестовый-модуль tests_generators.py
Содержит кейсы для тестирования функций модуля generators.py.
"""
import pytest

from src.generators import filter_by_currency
from tests.conftest import fixture_full_transactions


currency_codes = (
        'RUB', 'EUR', 'USD', 'AUD', 'AZN', 'AMD', 'BYN', 'BGN', 'BRL', 'HUF',
        'KRW', 'HKD', 'DKK', 'INR', 'KZT', 'CAD', 'KGS', 'CNY', 'MDL', 'TMT',
        'NOK', 'PLN', 'RON', 'SGD', 'TJS', 'TRY', 'UZS', 'UAH', 'GBP', 'CZK',
        'SEK', 'CHF', 'ZAR', 'JPY'
    )
"""
Примеры тест-кейсов

Тестирование функции filter_by_currency:
Напишите тесты, проверяющие, что функция корректно фильтрует транзакции по заданной валюте.
Проверьте, что функция правильно обрабатывает случаи, когда транзакции в заданной валюте отсутствуют.
Убедитесь, что генератор не завершается ошибкой при обработке пустого списка или списка без соответствующих валютных операций.

Тестирование функции transaction_descriptions:
Проверьте, что функция возвращает корректные описания для каждой транзакции.
Тестируйте работу функции с различным количеством входных транзакций, включая пустой список.

Тестирование генератора card_number_generator:
Напишите тесты, которые проверяют, что генератор выдает правильные номера карт в заданном диапазоне.
Проверьте корректность форматирования номеров карт.
Убедитесь, что генератор корректно обрабатывает крайние значения диапазона и правильно завершает генерацию.

Не забывайте использовать параметризацию и фикстуры в тестах для облегчения написания тестов и улучшения читаемости кода.
"""
transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "",
                    "code": ""
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        },
        {
            "id": "",
            "state": "",
            "date": "",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        },
        {
            None
        }
    ]

# Параметризованный тест.
@pytest.mark.parametrize(
    "transactions, filter_name",
    [
        (transactions[:], 'USD',),
        (transactions[:], 'RUB',),
        (transactions[2], '',),
        # (transactions[3], 'RUB',),
        # (transactions[4], 'RUB',),
        # (transactions[5], 'RUB',),
    ]
)
def test_filter_by_currency(transactions, filter_name) -> None:
    """Тест функции filter_by_currency"""
    if filter_name == '':
        raise ValueError('Ошибка вводимого значения')
    assert filter_name in currency_codes, f'Некорректные данные в имени валюты {filter_name}.'
    if filter_name == 'USD' or 'RUB':
        result = [filter_by_currency(transactions, filter_name)]
        assert len(result) == 1



def test_transaction_descriptions(fixture_full_transactions) -> None:
    """Тест функции transaction_descriptions"""


def test_number_generator(fixture_integer) -> None:
    """Тест функции number_generator"""


def test_card_number_generator(fixture_integer, fixture_separator: str = " ") -> None:
    """Тест функции card_number_generator"""