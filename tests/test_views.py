import json
from unittest.mock import patch

from src.views import generate_finance_report


# Тест для функции generate_finance_report
@patch("src.utils.get_greeting")
@patch("src.utils.get_card_statistics")
@patch("src.utils.get_top_transactions")
@patch("src.utils.get_currency_rates")
@patch("src.utils.get_stock_prices")
@patch("src.utils.load_user_settings")
def test_generate_finance_report(
    mock_get_greeting,
    mock_get_card_statistics,
    mock_get_top_transactions,
    mock_get_currency_rates,
    mock_get_stock_prices,
    mock_load_user_settings,
):
    mock_get_greeting.return_value = "Добрый день"
    mock_get_card_statistics.return_value = [{"last_digits": "3456", "total_spent": 3000.0, "cashback": 150.0}]
    mock_get_top_transactions.return_value = [{"amount": -5000, "category": "Еда", "description": "Ресторан"}]
    mock_get_currency_rates.return_value = [{"currency": "USD", "rate": 75.0}]
    mock_get_stock_prices.return_value = [{"stock": "AAPL", "price": 150.0}]
    mock_load_user_settings.return_value = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
    }

    data = {"data": []}  # Пустые данные для теста

    result = generate_finance_report(data)
    report = json.loads(result)

    assert "greeting" in report
    # assert report["greeting"] == "Добрый день"  # Проверяем приветствие
    assert "cards" in report
    assert len(report["cards"]) > 0  # Проверяем, что есть данные по картам
    assert "top_transactions" in report
    assert len(report["top_transactions"]) > 0  # Проверяем, что есть топ транзакций
    # assert "currency_rates" in report
    # assert len(report["currency_rates"]) > 0  # Проверяем, что есть данные по валютам
    # assert "stock_prices" in report
    # assert len(report["stock_prices"]) > 0  # Проверяем, что есть данные по акциям
