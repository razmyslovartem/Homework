from pytest import mark

from src.filtered_transactions import process_bank_operations
from src.filtered_transactions import process_bank_search


# Параметризованный тест.
@mark.parametrize(
    "operation",
    [
        {"id": 200634844, "date": "2018-02-13T04:43:11.374324", "description": "Перевод организации"},
        {"id": 121646999, "date": "2018-06-08T16:14:59.936274", "description": "Перевод организации"},
        {"id": 464419177, "date": "2018-07-15T18:44:13.346362", "description": "Перевод с карты на счет"},
        {"id": 594226727, "date": "2018-09-12T21:27:25.241689", "description": "Перевод организации"},
        {"id": 615064591, "date": "2018-10-14T08:21:33.419441", "description": "Перевод с карты на счет"},
    ],
)
def test_process_bank_search(operation: dict) -> None:
    """Тест функции process_bank_search"""

    """Тесты входных данных"""
    volume_description = str(operation["description"])

    assert "description" in operation
    assert volume_description is not None
    assert isinstance(volume_description, str)

    result_func = process_bank_search([operation], "с карты")

    assert isinstance(result_func, list)


def test_process_bank_operations(fixture_list_operations: list[dict]) -> None:
    """Тест функции process_bank_operations"""

    result_func = process_bank_operations(fixture_list_operations, ["Перевод организации"])

    assert isinstance(result_func, dict)
    assert "Перевод организации" in result_func
    assert result_func["Перевод организации"] == 3
