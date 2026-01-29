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


@pytest.fixture()
def fixture_card_numbers() -> str:
    """Фикстура для предоставления тестового номера карты"""
    return '7000792289606361'

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
    return '73654108430135874305'


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
        {
            "input": "Visa Platinum 7000792289603456",
            "expected": "Visa Platinum 7000 79** **** 3456"
        },
        {
            "input": "Maestro 7000792289606361",
            "expected": "Maestro 7000 79** **** 6361"
        },
        {
            "input": "МИР 1234567890123456",
            "expected": "МИР 1234 56** **** 3456"
        },
        {
            "input": "American Express 5555555555554444",
            "expected": "American Express 5555 55** **** 4444"
        },
        {
            "input": "Visa Classic 4000123456789010",
            "expected": "Visa Classic 4000 12** **** 9010"
        },
        {
            "input": 'Счет 73654108430135874305',
            "expected": 'Счет **4305',
        }
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
def test_operations_data():
    """Фикстура с тестовыми данными операций"""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 123456789, "state": "PENDING", "date": "2023-01-15T10:30:00.000000"},
    ]

@pytest.fixture
def empty_operations_data():
    """Фикстура с пустым списком операций"""
    return []

@pytest.fixture
def operations_without_state():
    """Фикстура с операциями без ключа 'state'"""
    return [
        {"id": 1, "date": "2023-01-01T00:00:00.000000"},
        {"id": 2, "date": "2023-01-02T00:00:00.000000"},
    ]







# @pytest.fixture
# def fixture_list_operations() -> list[dict[str, str | int]]:
#     """Возвращает список банковских операций словарями"""
#     return [
#         {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
#         {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
#         {"id": 132452323, "state": "CANCELED", "date": "2020-09-12T21:27:25.241689"},
#         {"id": 984357699, "state": "EXECUTED", "date": "2022-03-14T09:21:33.419441"},
#         {"id": 984394534, "state": "EXECUTED", "date": "2017-12-15T08:23:38.419456"},
#         {"id": 123432344, "state": "CANCELED", "date": "2023-11-18T20:11:31.455141"},
#         {"id": 234554322, "state": "EXECUTED", "date": "2025-01-14T08:21:36.519841"},
#         {"id": 768576858, "state": "EXECUTED", "date": "2025-01-14T10:25:33.317481"},
#     ]
#
# @pytest.fixture
# def fixture_full_transactions() -> list[dict]:
#     """Фикстура примера входных данных"""
#     transactions = [
#         {
#             "id": 939719570,
#             "state": "EXECUTED",
#             "date": "2018-06-30T02:08:58.425572",
#             "operationAmount": {
#                 "amount": "9824.07",
#                 "currency": {
#                     "name": "USD",
#                     "code": "USD"
#                 }
#             },
#             "description": "Перевод организации",
#             "from": "Счет 75106830613657916952",
#             "to": "Счет 11776614605963066702"
#         },
#         {
#             "id": 142264268,
#             "state": "EXECUTED",
#             "date": "2019-04-04T23:20:05.206878",
#             "operationAmount": {
#                 "amount": "79114.93",
#                 "currency": {
#                     "name": "USD",
#                     "code": "USD"
#                 }
#             },
#             "description": "Перевод со счета на счет",
#             "from": "Счет 19708645243227258542",
#             "to": "Счет 75651667383060284188"
#         },
#         {
#             "id": 873106923,
#             "state": "EXECUTED",
#             "date": "2019-03-23T01:09:46.296404",
#             "operationAmount": {
#                 "amount": "43318.34",
#                 "currency": {
#                     "name": "руб.",
#                     "code": "RUB"
#                 }
#             },
#             "description": "Перевод со счета на счет",
#             "from": "Счет 44812258784861134719",
#             "to": "Счет 74489636417521191160"
#         },
#         {
#             "id": 895315941,
#             "state": "EXECUTED",
#             "date": "2018-08-19T04:27:37.904916",
#             "operationAmount": {
#                 "amount": "56883.54",
#                 "currency": {
#                     "name": "",
#                     "code": ""
#                 }
#             },
#             "description": "Перевод с карты на карту",
#             "from": "Visa Classic 6831982476737658",
#             "to": "Visa Platinum 8990922113665229"
#         },
#         {
#             "id": 594226727,
#             "state": "CANCELED",
#             "date": "2018-09-12T21:27:25.241689",
#             "operationAmount": {
#                 "amount": "67314.70",
#                 "currency": {
#                     "name": "руб.",
#                     "code": "RUB"
#                 }
#             },
#             "description": "Перевод организации",
#             "from": "Visa Platinum 1246377376343588",
#             "to": "Счет 14211924144426031657"
#         }
#     ]
#     return transactions
#
#
# @pytest.fixture
# def fixture_card_strings_from_transactions() -> List[Dict[str, Any]]:
#     """Фикстура с картами из транзакций коллеги"""
#     return [
#         {
#             "input": "Visa Classic 6831982476737658",
#             "expected": "Visa Classic 6831 98** **** 7658",
#             "type": "card",
#             "state": "EXECUTED",
#             "date": "2018-08-19T04:27:37.904916"
#         },
#         {
#             "input": "Visa Platinum 8990922113665229",
#             "expected": "Visa Platinum 8990 92** **** 5229",
#             "type": "card",
#             "state": "EXECUTED",
#             "date": "2018-08-19T04:27:37.904916"
#         },
#         {
#             "input": "Visa Platinum 1246377376343588",
#             "expected": "Visa Platinum 1246 37** **** 3588",
#             "type": "card",
#             "state": "CANCELED",
#             "date": "2018-09-12T21:27:25.241689"
#         },
#     ]
#
# @pytest.fixture
# def fixture_account_strings_from_transactions() -> List[Dict[str, Any]]:
#     """Фикстура со счетами из транзакций коллеги"""
#     return [
#         {
#             "input": "Счет 75106830613657916952",
#             "expected": "Счет **6952",
#             "type": "account",
#             "state": "EXECUTED",
#             "date": "2018-06-30T02:08:58.425572"
#         },
#         {
#             "input": "Счет 11776614605963066702",
#             "expected": "Счет **6702",
#             "type": "account",
#             "state": "EXECUTED",
#             "date": "2018-06-30T02:08:58.425572"
#         },
#         {
#             "input": "Счет 19708645243227258542",
#             "expected": "Счет **8542",
#             "type": "account",
#             "state": "EXECUTED",
#             "date": "2019-04-04T23:20:05.206878"
#         },
#         {
#             "input": "Счет 75651667383060284188",
#             "expected": "Счет **4188",
#             "type": "account",
#             "state": "EXECUTED",
#             "date": "2019-04-04T23:20:05.206878"
#         },
#         {
#             "input": "Счет 14211924144426031657",
#             "expected": "Счет **1657",
#             "type": "account",
#             "state": "CANCELED",
#             "date": "2018-09-12T21:27:25.241689"
#         },
#     ]
#
#
# @pytest.fixture
# def fixture_mixed_transaction_data() -> List[Dict[str, Any]]:
#     """Фикстура со смешанными данными из транзакций для тестирования mask_account_card"""
#     return [
#         {
#             "from": "Visa Classic 6831982476737658",
#             "to": "Visa Platinum 8990922113665229",
#             "state": "EXECUTED",
#             "date": "2018-08-19T04:27:37.904916",
#             "expected_from": "Visa Classic 6831 98** **** 7658",
#             "expected_to": "Visa Platinum 8990 92** **** 5229",
#             "description": "Перевод с карты на карту"
#         },
#         {
#             "from": "Счет 75106830613657916952",
#             "to": "Счет 11776614605963066702",
#             "state": "EXECUTED",
#             "date": "2018-06-30T02:08:58.425572",
#             "expected_from": "Счет **6952",
#             "expected_to": "Счет **6702",
#             "description": "Перевод организации"
#         },
#         {
#             "from": "Visa Platinum 1246377376343588",
#             "to": "Счет 14211924144426031657",
#             "state": "CANCELED",
#             "date": "2018-09-12T21:27:25.241689",
#             "expected_from": "Visa Platinum 1246 37** **** 3588",
#             "expected_to": "Счет **1657",
#             "description": "Перевод организации"
#         },
#     ]
#
#
# @pytest.fixture
# def fixture_all_masking_cases() -> List[Dict[str, Any]]:
#     """Фикстура со всеми случаями для тестирования масок"""
#     return [
#         # Карты
#         {"type": "card", "input": "Visa Classic 6831982476737658", "expected": "Visa Classic 6831 98** **** 7658"},
#         {"type": "card", "input": "MasterCard 1234567890123456", "expected": "MasterCard 1234 56** **** 3456"},
#         {"type": "card", "input": "МИР 1234567890123456", "expected": "МИР 1234 56** **** 3456"},
#         # Счета
#         {"type": "account", "input": "Счет 75106830613657916952", "expected": "Счет **6952"},
#         {"type": "account", "input": "Счет 12345678901234567890", "expected": "Счет **7890"},
#         {"type": "account", "input": "Account 98765432109876543210", "expected": "Account **3210"},
#     ]
