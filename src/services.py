import json
import logging
import pandas as pd
import re


def get_search_by_mobile_numbers() -> str:
    """Возвращает транзакции, у которых есть в описании есть номер телефона, в виде JSON"""
    logging.basicConfig(
        level=logging.INFO,
        encoding="utf-8",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename="../services.log",
        filemode="w",
    )

    services_logger = logging.getLogger("app.services")

    excel_file = "../data/operations.xlsx"
    df = pd.read_excel(excel_file, engine="openpyxl")
    data = {"data": df.to_dict("records")}
    transactions = data["data"]
    services_logger.info("Получены исходные данные")
    phone_pattern = re.compile(
        r"(?:\+7|8|7)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}"
    )
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


if __name__ == "__main__":
    result = get_search_by_mobile_numbers()
    print(result)
