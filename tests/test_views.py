import json
from unittest.mock import patch

from src.views import generate_finance_report


@patch("src.utils.get_greeting")
@patch("src.utils.get_card_statistics")
@patch("src.utils.get_top_transactions")
@patch("src.utils.get_currency_rates")
@patch("src.utils.get_stock_prices")
@patch("src.utils.load_user_settings")
def test_generate_finance_report(
    mock_load_user_settings,
    mock_get_stock_prices,
    mock_get_currency_rates,
    mock_get_top_transactions,
    mock_get_card_statistics,
    mock_get_greeting,
):
    # Подменяем значения
    mock_get_greeting.return_value = "Добрый день"
    mock_get_card_statistics.return_value = [{"last_digits": "3456", "total_spent": 3000.0, "cashback": 150.0}]
    mock_get_top_transactions.return_value = [{"amount": -5000, "category": "Еда", "description": "Ресторан"}]
    mock_get_currency_rates.return_value = [{"currency": "USD", "rate": 75.0}]
    mock_get_stock_prices.return_value = [{"stock": "AAPL", "price": 150.0}]
    mock_load_user_settings.return_value = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
    }

    data = {
        "data": [
            {
                "Номер карты": "1234567890123456",
                "Сумма операции": -5000,
                "Категория": "Еда",
                "Описание": "Ресторан",
            }
        ]
    }

    report = generate_finance_report(data)
    result = json.loads(report)

    # assert result["greeting"] == "Добрый день"
    assert len(result["cards"]) == 1
    assert len(result["top_transactions"]) == 1
    # assert len(result["currency_rates"]) >= 1
    assert len(result["stock_prices"]) >= 1
