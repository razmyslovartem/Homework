"""
В модуле generators.py
генераторы для обработки данных транзакций.
"""

from typing import Iterator


def filter_by_currency(data_array_transactions: list[dict], filter_currency: str) -> Iterator:
    """
    Принимает массив данных в виде списка транзакций и возвращает итератор ленивых
    запросов, который поочередно выдает отфильтрованные по виду валюты транзакции.
    """
    for transaction_report in data_array_transactions:

        currency_transaction = transaction_report["operationAmount"]["currency"]["name"]

        if currency_transaction == filter_currency:
            yield transaction_report

        else:
            continue


def transaction_descriptions(data_array_transactions: list[dict]) -> Iterator:
    """
    Принимает массив данных в виде списка транзакций и возвращает описание
    каждой операции по очереди через генератор ленивых запросов.
    """
    for transaction_report in data_array_transactions:
        yield transaction_report["description"]


def numbers_generator(generated_value: int = 1) -> Iterator:
    """Генератор чисел, используется в def card_number_generator."""

    maximum_value = 9999999999999999

    while generated_value <= maximum_value:
        yield generated_value
        generated_value += 1


def card_number_generator(start_card_number: int, finish_card_number: int, separator: str = " ") -> Iterator:
    """
    Генерирует номера карт в диапазоне 0000 0000 0000 0001 до 9999 9999 9999 9999.
    В формате 4 группы по 4 цифры, разделитель по умолчанию пробел.
    Функция принимает начальное и конечное значение генераций, 3й показатель(разделитель) необязателен.
    """
    for generated_card_number in numbers_generator(start_card_number):

        if generated_card_number > finish_card_number:
            break

        account_length = f"{generated_card_number:016d}"  # Добавление нулей форматированием до 16 разрядов.

        format_card_number = separator.join(
            [account_length[num:num + 4] for num in range(0, len(account_length), 4)]
        )

        yield format_card_number
