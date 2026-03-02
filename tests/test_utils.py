from unittest.mock import mock_open
from unittest.mock import patch

from src.utils import read_json  # импортируем вашу функцию


def test_read_json_empty_list() -> None:
    """Тест с пустым списком"""
    with patch("builtins.open", mock_open(read_data="[]")):
        with patch("json.load", return_value=[]):
            result = read_json("fake_path.json")
            assert result == []


def test_read_json_not_list() -> None:
    """Тест, когда JSON содержит не список"""
    with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
        with patch("json.load", return_value={"key": "value"}):
            result = read_json("fake_path.json")
            assert result == []


def test_read_json_file_not_found() -> None:
    """Тест ошибки FileNotFoundError"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = read_json("fake_path.json")
        assert result == []
