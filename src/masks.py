def get_mask_card_number(card_number: str | int) -> str:
    """Функция, которая маскирует номер карты."""
    card_str = str(card_number)
    digits = ''.join(char for char in card_str if char.isdigit())

    if card_number is None:
        raise ValueError('Не корректные входные данные: получен None')

    if not digits:
        raise ValueError('Не корректные входные данные: номер не содержит цифр')

    if len(digits) != 16:
        raise ValueError('Не корректные входные данные: номер должен содержать 16 цифр')

    first_part = digits[:4]
    second_part = digits[4:6]
    last_part = digits[-4:]

    masked_number = f"{first_part} {second_part}** **** {last_part}"

    return masked_number


def get_mask_account(account_number: str) -> str:
    """Функция, которая маскирует номер счета."""
    mask_account = str(account_number)
    masked_account = f"**{mask_account[-4:]}"

    return masked_account
