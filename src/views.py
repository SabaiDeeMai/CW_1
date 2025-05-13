import json

from src.utils import (get_card_statistics, get_currency_rates, get_greeting, get_stock_prices, get_top_transactions,
                       main_logger)


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
