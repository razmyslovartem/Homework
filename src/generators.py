"""
Модуль generators.py содержит
генераторы для обработки данных транзакций.
"""

from typing import Iterator


def filter_by_currency(full_transactions: list, filter_name: str) -> Iterator:
    """
    Принимает на вход список словарей, представляющих транзакции.
    Возвращать итератор, который поочередно выдает транзакции, где валюта
    операции соответствует заданной.
    """
    for report in full_transactions:
        try:
            currency_name = report["operationAmount"]["currency"]["name"]
            if currency_name == filter_name:
                yield report
        except (KeyError, TypeError):
            continue


def transaction_descriptions(full_transactions: list) -> Iterator:
    """
    Принимает список словарей с транзакциями и возвращает описание
    каждой операции по очереди.
    """
    for report in full_transactions:
        descript_transaction = report["description"]
        try:
            yield descript_transaction
        except (KeyError, TypeError):
            continue


def number_generator(start: int = 1) -> Iterator:
    """Генератор 1-16 значных чисел."""
    limit_level = 9999999999999999  # Лимит 16-ти значного числа.
    while start <= limit_level:
        yield start
        start += 1


def card_number_generator(start: int, end: int, separator: str = " ") -> Iterator:
    """
    Генерирует числа в формате XXXX XXXX XXXX XXXX, где X — цифры номера карты,
    диапазоне генерации 0000 0000 0000 0001 до 9999 9999 9999 9999.
    Функция принимает начальное и конечное значения для генерации всего диапазона номеров.
    """
    for number in number_generator(start):
        if number > end:
            break

        format_number = f"{number:016d}"  # Форматирование через f-строку.
        num_mask = separator.join([format_number[num : num + 4] for num in range(0, len(format_number), 4)])
        yield num_mask


# # Примеры использования использования функций из модуля generators.py.
# transactions = [
#     {
#         "id": 939719570,
#         "state": "EXECUTED",
#         "date": "2018-06-30T02:08:58.425572",
#         "operationAmount": {
#             "amount": "9824.07",
#             "currency": {
#                 "name": "USD",
#                 "code": "USD"
#                 }
#             },
#         "description": "Перевод организации",
#         "from": "Счет 75106830613657916952",
#         "to": "Счет 11776614605963066702",
#     },
#     {
#         "id": 142264268,
#         "state": "EXECUTED",
#         "date": "2019-04-04T23:20:05.206878",
#         "operationAmount": {
#             "amount": "79114.93",
#             "currency": {
#                 "name": "USD",
#                 "code": "USD"
#                   }
#               },
#         "description": "Перевод со счета на счет",
#         "from": "Счет 19708645243227258542",
#         "to": "Счет 75651667383060284188",
#     },
#     {
#         "id": 158764563,
#         "state": "EXECUTED",
#         "date": "2019-04-04T23:20:05.206878",
#         "operationAmount": {
#             "amount": "1000.00",
#             "currency": {
#                 "name": "RUB",
#                 "code": "RUB"
#                   }
#               },
#         "description": "Перевод с карты на карту",
#         "from": "Счет 16808858243227258287",
#         "to": "Счет 76951664978790527195",
#     },
# ]
#
# if __name__ == "__main__":
#     # Получаем генератор транзакций.
#     result_filter = filter_by_currency(transactions, 'USD')
#
#     # Выводим все подходящие транзакции.
#     for currency_name in result_filter:
#         print(
#             f"ID: {currency_name['id']},"
#             f"Сумма: {currency_name['operationAmount']['amount']} {currency_name['operationAmount']['currency']['name']}"
#         )
#
# descriptions = transaction_descriptions(transactions)
# for _ in range(3):
#     print(next(descriptions))
#
# num = number_generator(9999999999999999)
# print(next(num))
# # print(next(num)) # StopIteration
#
# for card_number in card_number_generator(7079234523434560, 7079234523434567):
#     print(card_number)