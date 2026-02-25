"""
Файл test_data_extractor.py
Содержит кейсы для тестирования модуля data_extractor.py
"""

import os
from unittest.mock import Mock

from dotenv import load_dotenv
import pandas as pd
from pandas import DataFrame

from src.data_extractor import get_info_csv
from src.data_extractor import get_info_xlsx


def test_get_info_csv(fixture_transactions: DataFrame) -> None:
    """Тест функции get_info_csv"""
    load_dotenv()
    file_csv_path = os.getenv("FILE_PATH_CSV", "default_log_file.csv")

    # Мокаем pd.read_csv
    mock_read_csv = Mock(return_value=fixture_transactions)
    pd.read_csv = mock_read_csv

    # Вызываем тестируемую функцию
    result = get_info_csv(file_csv_path)

    # Проверки
    assert isinstance(result, list)
    assert isinstance(file_csv_path, str)
    # Проверяем, что результат не пустой (если должны быть данные)
    assert len(result) > 0
    # Проверяем структуру первого элемента, если есть данные
    if result:
        assert isinstance(result[0], dict)

    # Проверяем, что наш mock был вызван с правильным путем
    mock_read_csv.assert_called_once_with(file_csv_path, sep=";", encoding="utf-8")


def test_get_info_xlsx(fixture_transactions: DataFrame) -> None:
    """Тест функции get_info_xlsx"""
    load_dotenv()
    file_xlsx_path = os.getenv("FILE_PATH_XLSX", "default_log_file.xlsx")

    # Мокаем pd.read_excel
    mock_read_excel = Mock(return_value=fixture_transactions)
    pd.read_excel = mock_read_excel

    # Вызываем тестируемую функцию
    result = get_info_xlsx(file_xlsx_path)

    # Проверки
    assert isinstance(result, list)
    assert isinstance(file_xlsx_path, str)
    assert len(result) > 0
    if result:
        assert isinstance(result[0], dict)

    # Проверяем, что наш mock был вызван
    mock_read_excel.assert_called_once_with(file_xlsx_path)
