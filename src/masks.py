def get_mask_card_number(card_number: str | int) -> str:
    """Функция, которая маскирует номер карты."""
    card_str = str(card_number)
    digits = "".join(char for char in card_str if char.isdigit())

    if card_number is None:
        raise ValueError("Не корректные входные данные: получен None")

    if not digits:
        raise ValueError("Не корректные входные данные: номер не содержит цифр")

    if len(digits) != 16:
        raise ValueError("Не корректные входные данные: номер должен содержать 16 цифр")

    first_part = digits[:4]
    second_part = digits[4:6]
    last_part = digits[-4:]

    masked_number = f"{first_part} {second_part}** **** {last_part}"

    return masked_number


def get_mask_account(account_number: str | int) -> str:
    """Функция, которая маскирует номер счета."""
    if account_number is None:
        raise ValueError("получен None")

    if not isinstance(account_number, (str, int)):
        raise ValueError("Не корректный тип данных")

    account_str = str(account_number)

    if account_str == "":
        raise ValueError("Не корректные входные данные: номер не содержит цифр")

    if not account_str.isdigit():
        if any(char.isdigit() for char in account_str):
            raise ValueError("Не корректные входные данные: номер должен содержать только цифры")
        else:
            raise ValueError("Не корректные входные данные: номер не содержит цифр")

    if len(account_str) != 20:
        raise ValueError("Не корректные входные данные: номер должен содержать 20 цифр")

    masked_account = f"**{account_str[-4:]}"

    return masked_account
