"""
Тестовый-модуль tests_generators.py
Содержит кейсы для тестирования функций модуля generators.py.
"""

import pytest

from src.generators import card_number_generator
from src.generators import filter_by_currency
from src.generators import numbers_generator
from src.generators import transaction_descriptions

world_currency_codes: tuple = (
    "RUB",
    "USD",
    "EUR",
    "GBP",
    "JPY",
    "CHF",
    "CAD",
    "AUD",
    "NZD",
    "CNY",
    "INR",
    "KRW",
    "SGD",
    "MXN",
    "BRL",
    "HKD",
    "SAR",
    "THB",
    "AED",
    "SEK",
    "NOK",
    "DKK",
    "PLN",
    "HUF",
    "CZK",
    "DZD",
    "AMD",
    "BHD",
    "BGN",
    "GEL",
    "ILS",
    "KZT",
    "UZS",
    "PHP",
    "ZAR",
    "TRY",
    "UAH",
    "CZK",
    "RON",
    "HRK",
    "ISK",
    "MYR",
    "IDR",
    "VND",
    "THB",
    "QAR",
    "OMR",
    "KWD",
    "JOD",
    "LYD",
)

data_array_transactions: list[dict] = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "RUB", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "", "code": ""}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]


@pytest.mark.parametrize(
    "transactions, filter_currency, expected_result",
    [
        (data_array_transactions, "RUB", 1),
        (data_array_transactions, "EUR", 0),
        (data_array_transactions, "USD", 2),
        ([], "RUB", 0),
    ],
)
def test_filter_by_currency(transactions: list[dict], filter_currency: str, expected_result: int) -> None:
    """Тест функции filter_by_currency"""
    selected_transactions = list(filter_by_currency(transactions, filter_currency))

    assert len(selected_transactions) == expected_result, "Не корректная работа фильтрующей функции"
    assert filter_currency in world_currency_codes, f"Не корректный код валюты >> {filter_currency}."


@pytest.mark.parametrize(
    "transaction, expected_descriptions",
    [
        ([data_array_transactions[0]], "Перевод организации"),
        ([data_array_transactions[1]], "Перевод со счета на счет"),
        ([data_array_transactions[2]], "Перевод со счета на счет"),
        ([data_array_transactions[3]], "Перевод с карты на карту"),
        ([data_array_transactions[4]], "Перевод организации"),
    ],
)
def test_transaction_descriptions(transaction: list[dict], expected_descriptions: str) -> None:
    """Тест функции transaction_descriptions"""
    messages_description = transaction_descriptions(transaction)

    assert next(messages_description) == expected_descriptions


def test_number_generator() -> None:
    """Тест функции number_generator"""
    expected_dataset = [100, 101, 102, 103, 104, 105, 106, 107]
    on_generator = numbers_generator(100)
    get_data_nums = list(next(on_generator) for _ in range(8))

    assert expected_dataset == get_data_nums


format_dataset = [
    [
        "0000 0000 0000 0000",
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
    ],
    [
        "7079 2345 2343 4560",
        "7079 2345 2343 4561",
    ],
    [],
]


@pytest.mark.parametrize(
    "start_card_number, finish_card_number, format_dataset",
    [
        (0, 2, format_dataset[0]),
        (7079234523434560, 7079234523434561, format_dataset[1]),
        (10000000000000000, 10000000000000001, format_dataset[2]),
    ],
)
def test_card_number_generator(start_card_number: int, finish_card_number: int, format_dataset: list[str]) -> None:
    """Тест функции card_number_generator"""
    set_card_numbers = list(card_number_generator(start_card_number, finish_card_number))

    assert set_card_numbers == format_dataset
