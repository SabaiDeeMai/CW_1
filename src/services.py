import json
import logging
import re

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="../services.log",
    filemode="w",
)

services_logger = logging.getLogger("app.services")


def get_search_by_mobile_numbers(transactions_data: dict) -> str:
    """Возвращает транзакции, у которых есть в описании номер телефона, в виде JSON"""

    transactions = transactions_data["data"]
    services_logger.info("Получены исходные данные")
    phone_pattern = re.compile(r"(?:\+7|8|7)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}")
    search_results = []
    for tx in transactions:
        if not isinstance(tx, dict):
            continue

        description = tx.get("Описание")

        if pd.isna(description):
            continue

        description = str(description).strip()
        if not description:
            continue

        if phone_pattern.search(description):
            search_results.append(tx)

    services_logger.info("Поиск завершен")
    return json.dumps(search_results, ensure_ascii=False, indent=4)
