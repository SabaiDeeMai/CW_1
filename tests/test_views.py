import json
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.views import (
    get_greeting,
    get_card_statistics,
    get_top_transactions,
    get_currency_rates,
    get_stock_prices,
    generate_finance_report,
)


# Тест для функции get_greeting
def test_get_greeting():
    # Мокируем текущее время
    mock_time = datetime(2023, 5, 12, 10, 30)
    with patch("src.views.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_time
        mock_datetime.strptime.return_value = mock_time

        result = get_greeting()
        assert result == "Доброе утро"  # Ожидаем утреннее приветствие


# Тест для функции get_card_statistics
def test_get_card_statistics():
    transactions_data = {
        "data": [
            {
                "Номер карты": "1234567890123456",
                "Сумма операции": -1000,
                "Кэшбэк": 50,
                "Статус": "OK",
                "Валюта операции": "RUB",
                "Дата платежа": "12.05.2023",
            },
            {
                "Номер карты": "1234567890123456",
                "Сумма операции": -2000,
                "Кэшбэк": 100,
                "Статус": "OK",
                "Валюта операции": "RUB",
                "Дата платежа": "13.05.2023",
            },
            {
                "Номер карты": "9876543210987654",
                "Сумма операции": -500,
                "Кэшбэк": 20,
                "Статус": "OK",
                "Валюта операции": "RUB",
                "Дата платежа": "14.05.2023",
            },
        ]
    }

    result = get_card_statistics(transactions_data)
    assert len(result) == 2  # Должно быть 2 карты
    assert result[0]["last_digits"] == "3456"  # Проверяем последние 4 цифры карты
    assert result[0]["total_spent"] == 3000.0  # Проверяем общую сумму
    assert result[0]["cashback"] == 150.0  # Проверяем кэшбэк


# Тест для функции get_top_transactions
def test_get_top_transactions():
    transactions_data = {
        "data": [
            {"Сумма операции": -5000, "Дата платежа": "12.05.2023", "Категория": "Еда", "Описание": "Ресторан"},
            {"Сумма операции": -2000, "Дата платежа": "13.05.2023", "Категория": "Транспорт", "Описание": "Такси"},
            {"Сумма операции": -1500, "Дата платежа": "14.05.2023", "Категория": "Еда", "Описание": "Кафе"},
            {"Сумма операции": -3000, "Дата платежа": "15.05.2023", "Категория": "Транспорт", "Описание": "Проезд"},
            {"Сумма операции": -1000, "Дата платежа": "16.05.2023", "Категория": "Одежда", "Описание": "Магазин"},
            {"Сумма операции": -200, "Дата платежа": "17.05.2023", "Категория": "Еда", "Описание": "Перекус"},
        ]
    }

    result = get_top_transactions(transactions_data)
    assert len(result) == 5  # Ожидаем 5 транзакций
    assert result[0]["amount"] == -5000  # Проверяем сумму самой большой транзакции


# # Тест для функции get_currency_rates
# @patch("src.views.requests.get")
# def test_get_currency_rates(mock_get):
#     mock_response = MagicMock()
#     mock_response.json.return_value = {"rates": {"RUB": 75.0}}
#     mock_get.return_value = mock_response
#
#     # Мокируем load_user_settings
#     with patch("src.views.load_user_settings") as mock_load_user_settings:
#         mock_load_user_settings.return_value = {"user_currencies": ["USD", "EUR"]}
#
#         result = get_currency_rates()
#         assert len(result) == 2  # Должно быть 2 валюты
#         assert result[0]["currency"] == "USD"  # Проверка валюты
#         assert result[0]["rate"] == 75.0  # Проверка курса


# Тест для функции get_stock_prices
@patch("src.views.requests.get")
def test_get_stock_prices(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"meta": {"symbol": "AAPL"}, "values": [{"open": "150.00"}]}
    mock_get.return_value = mock_response

    # Мокируем load_user_settings
    with patch("src.views.load_user_settings") as mock_load_user_settings:
        mock_load_user_settings.return_value = {"user_stocks": ["AAPL"]}

        result = get_stock_prices()
        assert len(result) == 1  # Ожидаем 1 акцию
        assert result[0]["stock"] == "AAPL"  # Проверка символа акции
        # assert result[0]["price"] == 150.0  # Проверка цены


# Тест для функции generate_finance_report
@patch("src.views.get_greeting")
@patch("src.views.get_card_statistics")
@patch("src.views.get_top_transactions")
@patch("src.views.get_currency_rates")
@patch("src.views.get_stock_prices")
def test_generate_finance_report(
    mock_get_greeting,
    mock_get_card_statistics,
    mock_get_top_transactions,
    mock_get_currency_rates,
    mock_get_stock_prices,
):
    mock_get_greeting.return_value = "Добрый день"
    mock_get_card_statistics.return_value = [{"last_digits": "3456", "total_spent": 3000.0, "cashback": 150.0}]
    mock_get_top_transactions.return_value = [{"amount": -5000, "category": "Еда", "description": "Ресторан"}]
    mock_get_currency_rates.return_value = [{"currency": "USD", "rate": 75.0}]
    mock_get_stock_prices.return_value = [{"stock": "AAPL", "price": 150.0}]

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
