import json
from datetime import datetime
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from src.utils import (
    get_card_statistics,
    get_currency_rate,
    get_greeting,
    get_stock_prices,
    get_top_transactions,
    load_user_settings,
    read_excel_file,
    read_excel_file_to_df,
    get_currency_rates,
)


# Тесты для функции read_excel_file
@pytest.fixture
def excel_file_path():
    return "test_data.xlsx"


@pytest.fixture
def mock_excel_read():
    with patch("pandas.read_excel") as mock:
        yield mock


def test_read_excel_file_success(excel_file_path, mock_excel_read):
    mock_data = pd.DataFrame([{"Column1": "Value1", "Column2": "Value2"}])
    mock_excel_read.return_value = mock_data
    result = read_excel_file(excel_file_path)
    assert "data" in result
    assert isinstance(result["data"], list)
    assert result["data"][0]["Column1"] == "Value1"


def test_read_excel_file_error(excel_file_path, mock_excel_read):
    mock_excel_read.side_effect = Exception("Ошибка при чтении Excel")
    result = read_excel_file(excel_file_path)
    assert "error" in result
    assert "Ошибка при чтении Excel" in result["error"]


# Тесты для функции load_user_settings
def test_load_user_settings_success():
    mock_json = '{"setting1": "value1", "setting2": "value2"}'
    with patch("builtins.open", mock_open(read_data=mock_json)):
        result = load_user_settings("settings.json")
        assert result == json.loads(mock_json)


def test_load_user_settings_error():
    with patch("builtins.open", side_effect=Exception("Ошибка загрузки файла")):
        result = load_user_settings("../user_settings.json")
        assert result == {}  # Проверяем, что возвращается пустой словарь


# Тесты для функции get_currency_rate
@pytest.mark.parametrize(
    "currency_code, payment_date, expected_rate", [("USD", "24.05.2023", 75.0), ("EUR", "24.05.2023", 85.0)]
)
def test_get_currency_rate_success(currency_code, payment_date, expected_rate):
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"RUB": expected_rate}}
    with patch("requests.get", return_value=mock_response):
        result = get_currency_rate(currency_code, payment_date)
        assert result == expected_rate


def test_get_currency_rate_failure():
    with patch("requests.get", side_effect=Exception("API Error")):
        result = get_currency_rate("USD", "24.05.2023")
        assert result == 0.0


# Тесты для функции read_excel_file_to_df
@pytest.fixture
def mock_excel_read_to_df():
    with patch("pandas.read_excel") as mock:
        yield mock


def test_read_excel_file_to_df_success(mock_excel_read_to_df):
    mock_data = pd.DataFrame([{"Column1": "Value1", "Column2": "Value2"}])
    mock_excel_read_to_df.return_value = mock_data
    result = read_excel_file_to_df("test_data.xlsx")
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (1, 2)


def test_read_excel_file_to_df_error(mock_excel_read_to_df):
    mock_excel_read_to_df.side_effect = Exception("Ошибка при чтении Excel")
    result = read_excel_file_to_df("test_data.xlsx")
    assert "error" in result
    assert "Ошибка при чтении Excel" in result["error"]


# Тест для функции get_greeting
def test_get_greeting():
    # Мокируем текущее время
    mock_time = datetime(2023, 5, 12, 10, 30)
    with patch("src.utils.datetime") as mock_datetime:
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


# Тест для функции get_currency_rates
@patch("src.views.requests.get")
def test_get_currency_rates(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"RUB": 75.0}}
    mock_get.return_value = mock_response

    # Мокируем load_user_settings
    with patch("src.views.load_user_settings") as mock_load_user_settings:
        mock_load_user_settings.return_value = {"user_currencies": ["USD", "EUR"]}

        result = get_currency_rates()
        assert len(result) == 2  # Должно быть 2 валюты
        assert result[0]["currency"] == "USD"  # Проверка валюты
        assert result[0]["rate"] == 75.0  # Проверка курса


# Тест для функции get_stock_prices
@patch("src.utils.requests.get")
def test_get_stock_prices(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"meta": {"symbol": "AAPL"}, "values": [{"open": "150.00"}]}
    mock_get.return_value = mock_response

    # Мокируем load_user_settings
    with patch("src.utils.load_user_settings") as mock_load_user_settings:
        mock_load_user_settings.return_value = {"user_stocks": ["AAPL"]}

        result = get_stock_prices()
        assert len(result) == 1  # Ожидаем 1 акцию
        assert result[0]["stock"] == "AAPL"  # Проверка символа акции
        # assert result[0]["price"] == 150.0  # Проверка цены
