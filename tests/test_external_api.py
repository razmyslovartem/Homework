from typing import Optional
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import requests

from src.external_api import convert_transaction
from src.external_api import get_eur_to_rub_rate
from src.external_api import get_usd_to_rub_rate


# Тест для получения курса доллара
@patch("src.external_api.requests.get")
def test_get_usd_rate_success(mock_get: Mock) -> None:
    """Тест успешного получения курса доллара"""
    # Настраиваем мок
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True, "result": 75.50}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Подменяем API ключ
    with patch("src.external_api.API_KEY", "test_key"):
        rate: Optional[float] = get_usd_to_rub_rate()

        assert rate == 75.50
        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert",
            headers={"apikey": "test_key"},
            params={"from": "USD", "to": "RUB", "amount": 1},
            timeout=10,
        )


# Тест для получения курса евро
@patch("src.external_api.requests.get")
def test_get_eur_rate_success(mock_get: Mock) -> None:
    """Тест успешного получения курса евро"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True, "result": 85.30}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    with patch("src.external_api.API_KEY", "test_key"):
        rate: Optional[float] = get_eur_to_rub_rate()

        assert rate == 85.30
        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert",
            headers={"apikey": "test_key"},
            params={"from": "EUR", "to": "RUB", "amount": 1},
            timeout=10,
        )


# Тест отсутствия API ключа для USD
@patch("src.external_api.requests.get")
def test_get_usd_rate_no_api_key(mock_get: Mock) -> None:
    """Тест получения курса доллара без API ключа"""
    with patch("src.external_api.API_KEY", None):
        rate: Optional[float] = get_usd_to_rub_rate()
        assert rate is None
        mock_get.assert_not_called()


# Тест отсутствия API ключа для EUR
@patch("src.external_api.requests.get")
def test_get_eur_rate_no_api_key(mock_get: Mock) -> None:
    """Тест получения курса евро без API ключа"""
    with patch("src.external_api.API_KEY", None):
        rate: Optional[float] = get_eur_to_rub_rate()
        assert rate is None
        mock_get.assert_not_called()


# Тест ошибки запроса к API для USD
@patch("src.external_api.requests.get")
def test_get_usd_rate_request_exception(mock_get: Mock) -> None:
    """Тест ошибки запроса к API для доллара"""
    mock_get.side_effect = requests.exceptions.RequestException("Ошибка соединения")

    with patch("src.external_api.API_KEY", "test_key"):
        rate: Optional[float] = get_usd_to_rub_rate()
        assert rate is None


# Тест ошибки запроса к API для EUR
@patch("src.external_api.requests.get")
def test_get_eur_rate_request_exception(mock_get: Mock) -> None:
    """Тест ошибки запроса к API для евро"""
    mock_get.side_effect = requests.exceptions.RequestException("Ошибка соединения")

    with patch("src.external_api.API_KEY", "test_key"):
        rate: Optional[float] = get_eur_to_rub_rate()
        assert rate is None


# Тест ошибки обработки ответа от API для USD
@patch("src.external_api.requests.get")
def test_get_usd_rate_key_error(mock_get: Mock) -> None:
    """Тест ошибки обработки ответа API для доллара"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"wrong_key": "value"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    with patch("src.external_api.API_KEY", "test_key"):
        rate: Optional[float] = get_usd_to_rub_rate()
        assert rate is None


# Тест ошибки обработки ответа от API для EUR
@patch("src.external_api.requests.get")
def test_get_eur_rate_key_error(mock_get: Mock) -> None:
    """Тест ошибки обработки ответа API для евро"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"wrong_key": "value"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    with patch("src.external_api.API_KEY", "test_key"):
        rate: Optional[float] = get_eur_to_rub_rate()
        assert rate is None


# Тест ответа API с success=False для USD
@patch("src.external_api.requests.get")
def test_get_usd_rate_not_success(mock_get: Mock) -> None:
    """Тест ответа API с success=False для доллара"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": False}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    with patch("src.external_api.API_KEY", "test_key"):
        rate: Optional[float] = get_usd_to_rub_rate()
        assert rate is None


# Тест ответа API с success=False для EUR
@patch("src.external_api.requests.get")
def test_get_eur_rate_not_success(mock_get: Mock) -> None:
    """Тест ответа API с success=False для евро"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": False}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    with patch("src.external_api.API_KEY", "test_key"):
        rate: Optional[float] = get_eur_to_rub_rate()
        assert rate is None


# Тест общей ошибки для USD
@patch("src.external_api.requests.get")
def test_get_usd_rate_general_exception(mock_get: Mock) -> None:
    """Тест общей ошибки при получении курса доллара"""
    mock_get.side_effect = Exception("Неожиданная ошибка")

    with patch("src.external_api.API_KEY", "test_key"):
        rate: Optional[float] = get_usd_to_rub_rate()
        assert rate is None


# Тест общей ошибки для EUR
@patch("src.external_api.requests.get")
def test_get_eur_rate_general_exception(mock_get: Mock) -> None:
    """Тест общей ошибки при получении курса евро"""
    mock_get.side_effect = Exception("Неожиданная ошибка")

    with patch("src.external_api.API_KEY", "test_key"):
        rate: Optional[float] = get_eur_to_rub_rate()
        assert rate is None


# Тест конвертации USD с правильной структурой
@patch("src.external_api.get_usd_to_rub_rate")
def test_convert_usd_with_operation_amount(mock_get_rate: Mock) -> None:
    """Тест конвертации долларов в рубли с правильной структурой"""
    mock_get_rate.return_value = 75.50

    transaction = {"operationAmount": {"amount": 100, "currency": {"code": "USD"}}}
    result: Optional[float] = convert_transaction(transaction)

    assert result == 7550.0
    mock_get_rate.assert_called_once()


# Тест конвертации EUR с правильной структурой
@patch("src.external_api.get_eur_to_rub_rate")
def test_convert_eur_with_operation_amount(mock_get_rate: Mock) -> None:
    """Тест конвертации евро в рубли с правильной структурой"""
    mock_get_rate.return_value = 85.30

    transaction = {"operationAmount": {"amount": 200, "currency": {"code": "EUR"}}}
    result = convert_transaction(transaction)

    assert result == 17060.0
    mock_get_rate.assert_called_once()


# Тест транзакции в рублях с правильной структурой
def test_convert_rub_with_operation_amount() -> None:
    """Тест транзакции в рублях с правильной структурой"""
    transaction = {"operationAmount": {"amount": 1000, "currency": {"code": "RUB"}}}
    result = convert_transaction(transaction)

    assert result == 1000.0


# Тест отсутствия поля operationAmount
def test_missing_operation_amount() -> None:
    """Тест транзакции без поля operationAmount"""
    transaction = {"amount": 100, "currency": "USD"}
    result = convert_transaction(transaction)

    assert result is None


# Тест отсутствия поля amount в operationAmount
def test_missing_amount_in_operation_amount() -> None:
    """Тест отсутствия поля amount в operationAmount"""
    transaction = {"operationAmount": {"currency": {"code": "USD"}}}
    result = convert_transaction(transaction)

    assert result is None


# Тест отсутствия поля currency в operationAmount
def test_missing_currency_in_operation_amount() -> None:
    """Тест отсутствия поля currency в operationAmount"""
    transaction = {"operationAmount": {"amount": 100}}
    result = convert_transaction(transaction)

    assert result is None


# Тест отсутствия поля code в currency
def test_missing_code_in_currency() -> None:
    """Тест отсутствия поля code в currency"""
    transaction = {"operationAmount": {"amount": 100, "currency": {}}}
    result = convert_transaction(transaction)

    assert result is None


# Тест некорректной суммы в строке
def test_invalid_amount_string() -> None:
    """Тест с некорректной суммой в виде строки"""
    transaction = {"operationAmount": {"amount": "abc", "currency": {"code": "USD"}}}
    result = convert_transaction(transaction)

    assert result is None


# Тест некорректной суммы в виде None
def test_invalid_amount_none() -> None:
    """Тест с некорректной суммой в виде None"""
    transaction = {"operationAmount": {"amount": None, "currency": {"code": "USD"}}}
    result = convert_transaction(transaction)

    assert result is None


# Тест неподдерживаемой валюты с правильной структурой
def test_unsupported_currency_with_operation_amount() -> None:
    """Тест с неподдерживаемой валютой в правильной структуре"""
    transaction = {"operationAmount": {"amount": 100, "currency": {"code": "GBP"}}}
    result = convert_transaction(transaction)

    assert result is None


# Тест ошибки получения курса для USD
@patch("src.external_api.get_usd_to_rub_rate")
def test_convert_usd_rate_error(mock_get_rate: Mock) -> None:
    """Тест ошибки при получении курса доллара"""
    mock_get_rate.return_value = None

    transaction = {"operationAmount": {"amount": 100, "currency": {"code": "USD"}}}
    result = convert_transaction(transaction)

    assert result is None


# Тест ошибки получения курса для EUR
@patch("src.external_api.get_eur_to_rub_rate")
def test_convert_eur_rate_error(mock_get_rate: Mock) -> None:
    """Тест ошибки при получении курса евро"""
    mock_get_rate.return_value = None

    transaction = {"operationAmount": {"amount": 200, "currency": {"code": "EUR"}}}
    result = convert_transaction(transaction)

    assert result is None


# Тест ошибки KeyError при доступе к вложенным ключам
def test_key_error_in_nested_structure() -> None:
    """Тест KeyError при доступе к вложенным ключам"""
    transaction = {
        "operationAmount": {"amount": 100, "currency": "USD"}  # Неправильная структура, должно быть {"code": "USD"}
    }
    result = convert_transaction(transaction)

    assert result is None


# Тест TypeError при доступе к вложенным ключам
def test_type_error_in_nested_structure() -> None:
    """Тест TypeError при доступе к вложенным ключам"""
    transaction = {"operationAmount": "not a dict"}  # Неправильный тип данных
    result = convert_transaction(transaction)

    assert result is None
