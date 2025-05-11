import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Union

import pandas as pd
import requests
from dotenv import load_dotenv

from utils import get_currency_rate, load_user_settings

logging.basicConfig(
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="../application.log",
    filemode="w",
)

auth_logger = logging.getLogger("app.auth")
db_logger = logging.getLogger("app.database")
main_logger = logging.getLogger("app.main")


def get_greeting() -> str:
    """Возвращает приветствие в зависимости от времени"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S").time()
    auth_logger.info("Попытка входа для пользователя")
    if 6 <= time.hour < 12:
        return "Доброе утро"
    elif 12 <= time.hour < 17:
        return "Добрый день"
    elif 17 <= time.hour < 24:
        return "Добрый вечер"
    elif 0 <= time.hour < 6:
        return "Доброй ночи"
    else:
        auth_logger.warning("Неудачная попытка входа")
        return "Ошибка с получением времени"


def get_card_statistics(transactions_data: dict) -> List[Dict[str, Union[str, float]]]:
    """Обрабатывает JSON. По каждой карте выводит последние 4 цифры карты, общую сумму расходов, кэшбэк"""
    transactions = transactions_data["data"]
    db_logger.info("Получены исходные данные")
    cards_data = {}

    for tx in transactions:
        if not isinstance(tx, dict):
            continue

        card_number = tx.get("Номер карты")

        if pd.isna(card_number):
            continue

        if not str(card_number).strip() or not card_number:
            continue

        last_digits = str(card_number)[-4:]

        if last_digits not in cards_data:
            cards_data[last_digits] = {
                "last_digits": last_digits,
                "total_spent": 0.0,
                "cashback": 0.0,
            }

        # Суммируем траты и кэшбэк (с обработкой None), учитываем отмененные операции и валюту
        amount = (
            float(tx.get("Сумма операции", 0))
            if tx.get("Сумма операции") is not None
            else 0.0
        )
        cashback = float(tx.get("Кэшбэк", 0)) if tx.get("Кэшбэк") is not None else 0.0
        payment_status = tx.get("Статус", 0)
        transaction_currency = str(tx.get("Валюта операции", 0))
        date_of_payment = str(tx.get("Дата платежа", 0))

        if amount < 0 and payment_status == "OK":
            if transaction_currency != "RUB":
                amount = (
                    get_currency_rate(transaction_currency, date_of_payment) * amount
                )
            cards_data[last_digits]["total_spent"] = round(
                cards_data[last_digits]["total_spent"] + abs(amount), 2
            )

        if cashback > 0:
            cards_data[last_digits]["cashback"] += cashback

    return [
        {
            "last_digits": card["last_digits"],
            "total_spent": card["total_spent"],
            "cashback": card["cashback"],
        }
        for card in cards_data.values()
    ]


def get_top_transactions(transactions_data: dict) -> List[Dict[str, Union[str, float]]]:
    """Обрабатывает JSON. Выводит топ-5 транзакций по сумме платежа"""
    transactions = transactions_data["data"]
    db_logger.info("Получены исходные данные")
    cards_data = {}

    for tx in transactions:
        if not isinstance(tx, dict):
            continue

        operation_amount = tx.get("Сумма операции")
        operation_date = tx.get("Дата платежа")
        operation_category = tx.get("Категория") or ""
        if pd.isna(operation_category):  # Обработка pandas/numpy NaN
            operation_category = ""
        operation_description = tx.get("Описание")

        amount_key = abs(operation_amount)

        # Инициализируем запись для транзакции
        if amount_key not in cards_data:
            cards_data[operation_amount] = {
                "date": operation_date,
                "amount": operation_amount,
                "category": operation_category,
                "description": operation_description,
            }

    sorted_operation_amount = sorted(
        cards_data.values(), key=lambda op: abs(op["amount"]), reverse=True
    )

    return sorted_operation_amount[:5]


def get_currency_rates() -> List[Dict[str, Union[str, float]]]:
    """Выводит курс валют"""
    load_dotenv()
    db_logger.info("Загружен файл с ключами")
    api_key = os.getenv("API_KEY")
    api_url = "https://api.apilayer.com/exchangerates_data/latest"

    currencies_settings = load_user_settings("../user_settings.json")
    user_currencies = currencies_settings.get("user_currencies", [])

    headers = {"apikey": api_key}
    result = []
    for current_currency in user_currencies:
        payload = {"symbols": "RUB", "base": current_currency}

        try:
            response = requests.request("GET", api_url, headers=headers, params=payload)
            response.raise_for_status()
            currency_data = response.json()

            result.append(currency_data)
            if "rates" in currency_data and "RUB" in currency_data["rates"]:
                result.append(
                    {
                        "currency": current_currency,
                        "rate": round(float(currency_data["rates"]["RUB"]), 2),
                    }
                )

        except (requests.RequestException, KeyError, ValueError, TypeError, Exception):
            return [{}]
    return result if result else [{}]


def get_stock_prices() -> List[Dict[str, Union[str, float]]]:
    """Выводит курсы акций"""
    load_dotenv()
    db_logger.info("Загружен файл с ключами")
    twelvedata_api_key = os.getenv("TWELVEDATA_API_KEY")
    twelvedata_api_url = "https://api.twelvedata.com/time_series"

    stocks_settings = load_user_settings("../user_settings.json")
    user_stocks = stocks_settings.get("user_stocks", [])

    result = []
    for symbol in user_stocks:
        try:
            params = {
                "symbol": symbol,
                "interval": "1min",
                "apikey": twelvedata_api_key,
            }
            stock_api_response = requests.request(
                "GET", twelvedata_api_url, params=params
            )
            stock_api_response.raise_for_status()

            stock_data = stock_api_response.json()

            if "meta" in stock_data and "symbol" in stock_data["meta"]:
                result.append(
                    {
                        "stock": stock_data["meta"]["symbol"],
                        "price": round(float(stock_data["values"][0]["open"]), 2),
                    }
                )
        except (requests.RequestException, KeyError, ValueError, TypeError, Exception):
            db_logger.error("Неудачный запрос")
            return [{}]
    return result if result else [{}]


def generate_finance_report(data: dict) -> str:
    """Генерирует финансовый отчёт в формате JSON"""
    report = {
        "greeting": get_greeting(),
        "cards": get_card_statistics(data),
        "top_transactions": get_top_transactions(data),
        "currency_rates": get_currency_rates(),
        "stock_prices": get_stock_prices(),
    }
    main_logger.info("Отчет сформирован")
    return json.dumps(report, ensure_ascii=False, indent=4)
