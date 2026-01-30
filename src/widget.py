from datetime import datetime

from src.masks import get_mask_account
from src.masks import get_mask_card_number


def mask_account_card(type_account_card: str) -> str:
    """Функция, которая маскирует номер карты или счета."""
    if not isinstance(type_account_card, str):
        raise TypeError(f"Ожидалась строка, получен {type(type_account_card).__name__}")

    if not type_account_card.strip():
        raise ValueError("Передана пустая строка")

    string_account_card = type_account_card.strip().split()

    if len(string_account_card) < 2:
        raise ValueError("Строка должна содержать название и номер")

    name_parts = string_account_card[:-1]
    number_part = string_account_card[-1]

    digits_only = "".join([char for char in number_part if char.isdigit()])

    if len(digits_only) == 20:  # Это счет (20 цифр)
        masked_number = get_mask_account(number_part)
        mask_result = f"{' '.join(name_parts)} {masked_number}"
    elif len(digits_only) == 16:  # Это карта (16 цифр)
        masked_number = get_mask_card_number(number_part)
        mask_result = f"{' '.join(name_parts)} {masked_number}"
    else:
        # Определяем какое сообщение об ошибке показать
        if not digits_only:
            raise ValueError("Не корректные входные данные: номер не содержит цифр")
        elif len(digits_only) < 16:
            raise ValueError("Не корректные входные данные: номер должен содержать 16 или 20 цифр")
        else:
            raise ValueError(
                f"Не корректные входные данные: номер содержит {len(digits_only)} цифр, ожидается 16 или 20"
            )
    return mask_result


def get_date(date_str: str) -> str:
    """Функция, которая меняет формат даты ISO 8601 на 'ДД.ММ.ГГГГ'."""
    # Преобразуем строку в объект datetime
    dt = datetime.fromisoformat(date_str)

    # Форматируем в нужный формат
    return dt.strftime("%d.%m.%Y")
