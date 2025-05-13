import pytest
from unittest.mock import patch, MagicMock
import json
import pandas as pd
from src.utils import read_excel_file, load_user_settings, get_currency_rate, read_excel_file_to_df
from unittest.mock import patch, MagicMock, mock_open


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
        result = load_user_settings("settings.json")
        assert result == {}


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
