from unittest.mock import patch, MagicMock
from src.external_api import get_usd_to_rub_rate, get_eur_to_rub_rate, convert_transaction


# Тест для получения курса доллара
@patch('src.external_api.requests.get')
def test_get_usd_rate_success(mock_get):
    """Тест успешного получения курса доллара"""
    # Настраиваем мок
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'success': True,
        'result': 75.50
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Подменяем API ключ
    with patch('src.external_api.API_KEY', 'test_key'):
        rate = get_usd_to_rub_rate()

        assert rate == 75.50
        mock_get.assert_called_once()


# Тест для получения курса евро
@patch('src.external_api.requests.get')
def test_get_eur_rate_success(mock_get):
    """Тест успешного получения курса евро"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'success': True,
        'result': 85.30
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    with patch('src.external_api.API_KEY', 'test_key'):
        rate = get_eur_to_rub_rate()

        assert rate == 85.30
        mock_get.assert_called_once()


# Тест ошибки API
@patch('src.external_api.requests.get')
def test_get_rate_api_error(mock_get):
    """Тест ошибки при запросе к API"""
    mock_get.side_effect = Exception("Ошибка соединения")

    with patch('src.external_api.API_KEY', 'test_key'):
        rate = get_usd_to_rub_rate()

        assert rate is None


# Тест конвертации USD
@patch('src.external_api.get_usd_to_rub_rate')
def test_convert_usd(mock_get_rate):
    """Тест конвертации долларов в рубли"""
    mock_get_rate.return_value = 75.50

    transaction = {'amount': 100, 'currency': 'USD'}
    result = convert_transaction(transaction)

    assert result == 7550.0
    mock_get_rate.assert_called_once()


# Тест конвертации EUR
@patch('src.external_api.get_eur_to_rub_rate')
def test_convert_eur(mock_get_rate):
    """Тест конвертации евро в рубли"""
    mock_get_rate.return_value = 85.30

    transaction = {'amount': 200, 'currency': 'EUR'}
    result = convert_transaction(transaction)

    assert result == 17060.0
    mock_get_rate.assert_called_once()


# Тест транзакции в рублях
def test_convert_rub():
    """Тест транзакции в рублях (без конвертации)"""
    transaction = {'amount': 1000, 'currency': 'RUB'}
    result = convert_transaction(transaction)

    assert result == 1000.0


# Тест отсутствия поля amount
def test_missing_amount():
    """Тест транзакции без поля amount"""
    transaction = {'currency': 'USD'}
    result = convert_transaction(transaction)

    assert result is None


# Тест отсутствия поля currency
def test_missing_currency():
    """Тест транзакции без поля currency"""
    transaction = {'amount': 100}
    result = convert_transaction(transaction)

    assert result is None


# Тест неподдерживаемой валюты
def test_unsupported_currency():
    """Тест с неподдерживаемой валютой"""
    transaction = {'amount': 100, 'currency': 'GBP'}
    result = convert_transaction(transaction)

    assert result is None


# Тест некорректной суммы
def test_invalid_amount():
    """Тест с некорректной суммой"""
    transaction = {'amount': 'abc', 'currency': 'USD'}
    result = convert_transaction(transaction)

    assert result is None


# Тест ошибки получения курса
@patch('src.external_api.get_usd_to_rub_rate')
def test_convert_rate_error(mock_get_rate):
    """Тест ошибки при получении курса"""
    mock_get_rate.return_value = None

    transaction = {'amount': 100, 'currency': 'USD'}
    result = convert_transaction(transaction)

    assert result is None
