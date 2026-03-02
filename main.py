import os

import pandas as pd
from dotenv import load_dotenv

from src.data_extractor import get_info_csv, get_info_xlsx
from src.filtered_transactions import process_bank_search
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.utils import read_json
from src.widget import get_date, mask_account_card


def main() -> None:
    ai_prefix = "\033[36mПрограмма:\033[0m"
    user_prefix = "\033[92mПользователь: \033[0m"
    menu_item = None
    status = None
    answer_sort = None
    direction = None
    answer_currency = None
    answer_search = None

    # Опрос для выдачи результата:
    # Вопрос №1 откуда берем данные.

    print(
        f"""{ai_prefix} Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n
        Выберите необходимый пункт меню:
        1. Получить информацию о транзакциях из JSON-файла
        2. Получить информацию о транзакциях из CSV-файла
        3. Получить информацию о транзакциях из XLSX-файла\n"""
    )

    while menu_item not in ["1", "2", "3"]:
        menu_item = input(user_prefix)

    name_file = {"1": "JSON", "2": "CSV", "3": "XLSX"}

    if menu_item == "1":
        transactions = read_json(file_json_path)
    elif menu_item == "2":
        transactions = get_info_csv(file_csv_path)
    else:
        transactions = get_info_xlsx(file_xlsx_path)

    for transaction in transactions:
        print(transaction)

    print(f"\n{ai_prefix}({len(transactions)}) Для обработки выбран {name_file[menu_item]}-файл.\n")

    # Вопрос №2 выбор статуса интересующих операций.

    print(
        f"""{ai_prefix} Выберите статус, по которому необходимо выполнить фильтрацию.\n
        Выберите необходимый пункт меню:
        1. EXECUTED
        2. CANCELED
        3. PENDING
        * или введите статус вручную, регистр неважен.\n"""
    )

    while status not in ["1", "2", "3", "EXECUTED", "CANCELED", "PENDING"]:
        status = input(user_prefix).upper()
    print()

    if status.isdigit():
        name_status = {"1": "EXECUTED", "2": "CANCELED", "3": "PENDING"}
        flag_status = name_status[status]
    else:
        flag_status = status

    transactions = filter_by_state(transactions, flag_status)

    for transaction in transactions:
        print(transaction)

    print(f'\n{ai_prefix}({len(transactions)}) Операции отфильтрованы по статусу "{flag_status}".\n')

    # Вопрос №3 уточнения выборки операций сортировки.

    print(
        f"""{ai_prefix} Отсортировать операции по дате? Да/Нет\n
        Выберите необходимый пункт меню:
        1. Да
        2. Нет
        * или введите ответ вручную, регистр неважен.\n"""
    )

    while answer_sort not in ["1", "2", "ДА", "НЕТ"]:
        answer_sort = input(user_prefix).upper()

    if answer_sort == "1" or answer_sort == "ДА":

        print(
            f"""\n{ai_prefix} Отсортировать по возрастанию или по убыванию?\n
        Выберите необходимый пункт меню:
        1. по возрастанию
        2. по убыванию\n"""
        )

        while direction not in ["1", "2"]:
            direction = input(user_prefix)
        print()

        if direction == "1":
            sorting_direction = False
            text_direction = "по возрастанию"

        else:
            sorting_direction = True
            text_direction = "по убыванию"

        transactions = sort_by_date(transactions, sorting_direction)

        for transaction in transactions:
            print(transaction)

        print(f"\n{ai_prefix} Отсортирован {text_direction}.\n")

    else:

        print(f"\n{ai_prefix} Сортировка по дате не применялась.\n")

    # Вопрос №4 фильтрация по валюте.

    print(
        f"""{ai_prefix} Выводить только рублевые транзакции? Да/Нет\n
        Выберите необходимый пункт меню:
        1. Да
        2. Нет\n"""
    )

    while answer_currency not in ["1", "2"]:
        answer_currency = input(user_prefix)
    print()

    if answer_currency == "1":
        transactions = filter_by_currency(transactions, "RUB")
        # Переводим тип данных из генератора в лист, иначе данные пропадут
        # когда генератор закончится.
        transactions = list(transactions)

        for transaction in transactions:
            print(transaction)

        print(f"\n{ai_prefix}({len(transactions)}) Произведена фильтрация по валюте.\n")

    else:
        print(f"\n{ai_prefix}({len(transactions)}) Фильтрация по валюте не производилась.")

    # Вопрос №5 фильтрация по фабуле в описании трансакций.

    print(
        f"""\n{ai_prefix} Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n
        Выберите необходимый пункт меню:
        1. Да
        2. Нет\n"""
    )

    while answer_search not in ["1", "2"]:
        answer_search = input(user_prefix)
    print()

    long_txs = len(transactions)
    if answer_search == "1":
        answer_text = input("\nВведи текст для поиска:\n")

        transactions = process_bank_search(transactions, answer_text)

        if long_txs == 0:
            print(
                f"""\n{ai_prefix}({long_txs}) Не найдено ни одной транзакции, подходящей
           под ваши условия фильтрации!!!"""
            )

    else:

        print(f"\n{ai_prefix} Фильтрация по тексту не производилась.\n")

    # Голова отчёта
    print("+" + "-" * 60 + "+")
    print(f"\n{ai_prefix} Распечатываю итоговый список транзакций...\n")
    print(f"Всего банковских операций в выборке: {long_txs}\n")

    for transaction in transactions:
        # 1. Дата
        date_str = get_date(transaction["date"])

        # 2. Описание
        text_str = transaction["description"]

        # 3. Поле "from" (может отсутствовать)
        from_value = transaction.get("from", "")
        from_str = str(from_value) if pd.notna(from_value) else ""
        mask_from = mask_account_card(from_str) if from_str else "Не указано"

        # 4. Поле "to" (может отсутствовать)
        to_value = transaction.get("to", "")
        to_str = str(to_value) if pd.notna(to_value) else ""
        mask_to = mask_account_card(to_str) if to_str else "Не указано"

        # 5. Сумма
        if "amount" in transaction:
            amount_money = float(transaction["amount"])
        else:
            amount_money = float(transaction["operationAmount"]["amount"])

        # 6. Валюта
        if "currency_code" in transaction:
            currency_code = transaction["currency_code"]
        else:
            currency_code = transaction["operationAmount"]["currency"]["code"]

        # Вывод
        print(f"{date_str} {text_str.lower()}")
        print(f"{mask_from} -> {mask_to}")
        print(f"Сумма: {int(amount_money)} {currency_code}")
        print("`" * 62)


load_dotenv()  # Загрузка переменных из .env-файла.
file_json_path = os.getenv("FILE_PATH", "default_log_file.json")
file_csv_path = os.getenv("FILE_PATH_CSV", "default_log_file.csv")
file_xlsx_path = os.getenv("FILE_PATH_XLSX", "default_log_file.xlsx")

main()
print("Выборка данных закончена.")
print("+" + "-" * 60 + "+")
