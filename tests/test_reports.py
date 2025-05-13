import json
import pytest
import pandas as pd
from unittest.mock import patch
from src.reports import spending_by_category


# Фикстура для подготовки тестовых данных
@pytest.fixture
def test_data():
    return pd.DataFrame(
        {
            "Категория": ["Категория1", "Категория1", "Категория2"],
            "Сумма операции": [-1000, -2000, 3000],
            "Дата платежа": ["01.02.2025", "15.03.2025", "20.04.2025"],
            "Статус": ["OK", "OK", "OK"],
            "Валюта операции": ["RUB", "RUB", "RUB"],  # Все данные в рублях
        }
    )


# Параметризированный тест
@pytest.mark.parametrize(
    "chosen_category, expected_total",
    [
        ("Категория1", 2000.0),  # В расчет до сегодня попадет только второй платеж
        ("Категория2", 0.0),  # Категория2 не имеет операций с отрицательной суммой
    ],
)
def test_spending_by_category(test_data, chosen_category, expected_total):
    # Мокируем функцию get_currency_rate, чтобы она не выполнялась
    with patch("src.reports.get_currency_rate") as mock_get_currency_rate:
        mock_get_currency_rate.return_value = 1.0  # Возвращаем 1.0 для конвертации, чтобы не менять суммы

        # Вызываем функцию
        result = spending_by_category(test_data, chosen_category)

        # Десериализуем JSON результат
        result_value = json.loads(result)

        # Проверка результата
        assert isinstance(result_value, float)
        assert result_value == expected_total
