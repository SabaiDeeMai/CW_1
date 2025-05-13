import json
from unittest.mock import patch

import pytest

from src.services import get_search_by_mobile_numbers


@pytest.fixture
def sample_transactions():
    return {
        "data": [
            {"Описание": "Перевод на номер +7 999 123-45-67"},
            {"Описание": "Оплата 89001234567 за интернет"},
            {"Описание": "Покупка кофе"},
            {"Описание": None},
            {"Описание": "   "},
            {"Описание": "Звонок другу 74951234567"},
        ]
    }


@pytest.mark.parametrize(
    "description,should_match",
    [
        ("Перевод +7 999 123-45-67", True),
        ("Связь 8 (999) 123 45 67", True),
        ("Пополнение 89001234567", True),
        ("Карта 74951234567", True),
        ("Без телефона", False),
        (None, False),
        ("", False),
        ("   ", False),
    ],
)
def test_phone_filtering(description, should_match):
    tx_data = {"data": [{"Описание": description}]}

    with patch("src.services.services_logger") as mock_logger:
        result_json = get_search_by_mobile_numbers(tx_data)
        result = json.loads(result_json)

        if should_match:
            assert len(result) == 1
            assert result[0]["Описание"] == description
        else:
            assert result == []

        mock_logger.info.assert_any_call("Получены исходные данные")
        mock_logger.info.assert_any_call("Поиск завершен")


def test_full_data_processing(sample_transactions):
    with patch("src.services.services_logger") as mock_logger:
        result_json = get_search_by_mobile_numbers(sample_transactions)
        result = json.loads(result_json)

        assert len(result) == 3

        phones = [tx["Описание"] for tx in result]
        assert any("+7 999 123-45-67" in p for p in phones)
        assert any("89001234567" in p for p in phones)
        assert any("74951234567" in p for p in phones)

        mock_logger.info.assert_called_with("Поиск завершен")
