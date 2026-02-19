import logging
import os

# Переменные для формирования точного пути до лог-файла.
path_inside_project = os.path.dirname(os.path.abspath(__file__))
path_inside_logs = "../logs/masks.log"

# Создаем путь до файла логов относительно текущей директории.
full_path = os.path.join(path_inside_project, path_inside_logs)
abs_path = os.path.abspath(full_path)

logger = logging.getLogger("masks")  # pragma: no cover
logger.setLevel(logging.DEBUG)  # pragma: no cover
file_handler = logging.FileHandler(filename=abs_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str | int | None) -> str:
    """Функция, которая маскирует номер карты."""
    logger.info(f"Накладываем маску на номер карты: {card_number}")

    if card_number is None:
        logger.error("Не корректные входные данные: получен None")
        raise ValueError("Не корректные входные данные: получен None")

    card_str = str(card_number)
    digits = "".join(char for char in card_str if char.isdigit())

    if not digits:
        logger.error("Не корректные входные данные: номер не содержит цифр")
        raise ValueError("Не корректные входные данные: номер не содержит цифр")

    if len(digits) != 16:
        logger.error("Не корректные входные данные: номер должен содержать 16 цифр")
        raise ValueError("Не корректные входные данные: номер должен содержать 16 цифр")

    first_part = digits[:4]
    second_part = digits[4:6]
    last_part = digits[-4:]

    masked_number = f"{first_part} {second_part}** **** {last_part}"
    logger.info(f"Маска номера карты на выходе: {masked_number}")
    return masked_number


def get_mask_account(account_number: str | int | None | list | dict) -> str:
    """Функция, которая маскирует номер счета."""
    logger.info(f"Накладываем маску на номер счёта: {account_number}")
    if account_number is None:
        logger.error("получен None")
        raise ValueError("получен None")

    if not isinstance(account_number, (str, int)):
        logger.error("Не корректный тип данных")
        raise ValueError("Не корректный тип данных")

    account_str = str(account_number)

    if account_str == "":
        logger.error("Не корректные входные данные: номер не содержит цифр")
        raise ValueError("Не корректные входные данные: номер не содержит цифр")

    if not account_str.isdigit():
        logger.error("Не корректные входные данные")
        if any(char.isdigit() for char in account_str):
            raise ValueError("Не корректные входные данные: номер должен содержать только цифры")
        else:
            raise ValueError("Не корректные входные данные: номер не содержит цифр")

    if len(account_str) != 20:
        logger.error("Не корректные входные данные")
        raise ValueError("Не корректные входные данные: номер должен содержать 20 цифр")

    masked_account = f"**{account_str[-4:]}"
    logger.info(f"Маска номера счёта на выходе: {masked_account}")
    return masked_account


if __name__ == "__main__":  # pragma: no cover
    card_number = "7000792289606361"
    account_number = "73654108430135874305"

    print(get_mask_card_number(card_number))
    print(get_mask_account(account_number))
