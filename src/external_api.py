import os
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from dotenv import load_dotenv
import requests

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем API ключ из переменных окружения
API_KEY: Optional[str] = os.getenv("EXCHANGE_RATES_API_KEY")

API_URL: str = "https://api.apilayer.com/exchangerates_data/convert"


def get_usd_to_rub_rate() -> Optional[float]:
    """
    Получает текущий курс доллара к рублю
    """
    # Проверяем, есть ли API ключ
    if not API_KEY:
        print("Ошибка: не найден API ключ. Добавьте его в файл .env")
        return None

    try:
        # Заголовки для авторизации
        headers: Dict[str, str] = {"apikey": API_KEY}

        # Параметры запроса
        params: Dict[str, Union[str, int]] = {"from": "USD", "to": "RUB", "amount": 1}

        # Отправляем запрос к API
        url: str = f"{API_URL}"
        print("Отправляем запрос к API...")  # Для отладки
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Проверяем, что запрос успешен

        # Получаем данные из ответа
        data: Dict[str, Any] = response.json()

        # Проверяем, что запрос выполнен успешно
        if data.get("success"):
            rate = float(data["result"])
            print(f"Получен курс USD/RUB: {rate}")  # Для отладки
            return rate
        else:
            print("Ошибка при получении курса доллара")
            return None

    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None


def get_eur_to_rub_rate() -> Optional[float]:
    """
    Получает текущий курс евро к рублю
    """
    # Проверяем, есть ли API ключ
    if not API_KEY:
        print("Ошибка: не найден API ключ. Добавьте его в файл .env")
        return None

    try:
        headers: Dict[str, str] = {"apikey": API_KEY}

        params: Dict[str, Union[str, int]] = {"from": "EUR", "to": "RUB", "amount": 1}

        url: str = f"{API_URL}"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data: Dict[str, Any] = response.json()

        if data.get("success"):
            return float(data["result"])
        else:
            print("Ошибка при получении курса евро")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None


def convert_transaction(transaction: Dict[str, Any]) -> Optional[float]:
    """
    Принимает транзакцию и возвращает сумму в рублях

    Транзакция - это словарь вида:
    {'amount': 100, 'currency': 'USD'}
    {'amount': 150.50, 'currency': 'EUR'}
    {'amount': 5000, 'currency': 'RUB'}
    """

    # Проверяем, что в транзакции есть нужные поля
    if "amount" not in transaction:
        print("Ошибка: в транзакции нет поля 'amount'")
        return None

    if "currency" not in transaction:
        print("Ошибка: в транзакции нет поля 'currency'")
        return None

    # Получаем сумму и валюту
    amount = transaction["amount"]
    currency = transaction["currency"].upper()  # переводим в верхний регистр

    # Пробуем преобразовать сумму в число
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        print(f"Ошибка: не удалось преобразовать '{amount}' в число")
        return None

    # Если валюта - рубли, просто возвращаем сумму
    if currency == "RUB":
        return amount

    # Конвертируем доллары в рубли
    if currency == "USD":
        rate = get_usd_to_rub_rate()
        if rate is None:
            print("Не удалось получить курс доллара")
            return None
        rub_amount = amount * rate
        return rub_amount

    # Конвертируем евро в рубли
    if currency == "EUR":
        rate = get_eur_to_rub_rate()
        if rate is None:
            print("Не удалось получить курс евро")
            return None
        rub_amount = amount * rate
        return rub_amount

    # Если валюта не поддерживается
    print(f"Валюта {currency} не поддерживается. Поддерживаются: USD, EUR, RUB")
    return None


# Функция для демонстрации работы
def main() -> None: # pragma: no cover
    """
    Примеры использования функции
    """

    # Проверяем, есть ли API ключ
    if not API_KEY:
        print("=" * 50)
        print("ВНИМАНИЕ: Не найден API ключ!")
        print("=" * 50)
        print("\nЧтобы использовать программу:")
        print("1. Зарегистрируйтесь на https://apilayer.com/")
        print("2. Получите бесплатный API ключ")
        print("3. Создайте файл .env в той же папке")
        print("4. Добавьте в файл .env строку:")
        print("   EXCHANGE_RATES_API_KEY=ваш_ключ_сюда")
        print("\nПример запуска с тестовыми данными:")

    # Создаем несколько тестовых транзакций
    transactions: list[Dict[str, Any]] = [
        {"amount": 100, "currency": "USD"},
        {"amount": 150.50, "currency": "EUR"},
        {"amount": 5000, "currency": "RUB"},
        {"amount": "50", "currency": "USD"},  # строка тоже работает
        {"amount": 200, "currency": "GBP"},  # неподдерживаемая валюта
    ]

    # Обрабатываем каждую транзакцию
    for trans in transactions:
        print(f"\nОбрабатываем транзакцию: {trans['amount']} {trans['currency']}")

        result: Optional[float] = convert_transaction(trans)

        if result is not None:
            print(f"Сумма в рублях: {result:.2f} RUB")
        else:
            print("Не удалось обработать транзакцию")


if __name__ == "__main__":
    main()
