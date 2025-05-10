import pandas as pd
import requests
from dotenv import load_dotenv
import json
import os


def read_excel_file(file_path: str) -> dict:
    """Читает данные из Excel-файла и возвращает словарь с данными.

    Args:
        file_path: Путь к Excel-файлу

    Returns:
        Словарь с ключами:
        - 'data': список словарей с данными (в случае успеха)
        - 'error': сообщение об ошибке (при возникновении исключения)
    """
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        data = df.to_dict('records')

        return {
            "data": data
        }

    except Exception as e:
        return {
            "error": f"Ошибка при чтении Excel: {str(e)}"
        }


def load_user_settings(file_path: str) -> dict:
    """Загружает настройки из JSON файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки файла {file_path}: {str(e)}")
        return {}


def get_currency_rate(currency_code: str, payment_date: str) -> float:
    """Получает курс валюты к рублю на указанную дату

    Args:
        currency_code (str): Код валюты из 3 букв ('USD', 'EUR' и т.д.)
        payment_date (str): Дата в формате 'ДД.ММ.ГГГГ' (например '24.05.2023')

    Returns:
        float: Курс валюты к RUB или 0.0 при ошибке
    """
    load_dotenv()
    try:
        day, month, year = payment_date.split('.')
        formatted_date = f"{year}-{month}-{day}"

        api_key = os.getenv('API_KEY')

        url = f"https://api.apilayer.com/exchangerates_data/{formatted_date}"
        params = {
            "symbols": "RUB",
            "base": currency_code
        }
        headers = {"apikey": api_key}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        return float(data['rates']['RUB'])

    except Exception:
        return 0.0
