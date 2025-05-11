import datetime
import json
import logging
from functools import wraps
from typing import Callable, Optional

import pandas as pd
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from src.utils import get_currency_rate

# Настройка логгера
reports_logger = logging.getLogger("app.reports")
reports_logger.setLevel(logging.INFO)

if not reports_logger.handlers:
    file_handler = logging.FileHandler(filename="../reports.log", encoding="utf-8", mode="w")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    reports_logger.addHandler(file_handler)


def save_report_to_file(filename: Optional[str] = None):
    """
    Декоратор для сохранения результатов функции в файл.

    Если имя файла не указано, генерируется автоматически в формате:
    'spending_report_YYYY-MM-DD.txt'
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Генерация имени файла, если не указано
            if filename is None:
                report_filename = f"spending_report_{datetime.date.today()}.txt"
            else:
                report_filename = filename

            # Запись результата в файл
            try:
                with open(report_filename, "w", encoding="utf-8") as f:
                    result_value = json.loads(result)

                    f.write(f"Отчет сгенерирован: {datetime.datetime.now()}\n")
                    f.write(f"Функция: {func.__name__}\n")
                    f.write(f"Категория: {kwargs.get('chosen_category', args[1] if len(args) > 1 else 'N/A')}\n")
                    f.write(f"Период: последние 3 месяца до {kwargs.get('end_date', 'текущей даты')}\n")
                    if isinstance(result_value, (float, int)):
                        f.write(f"Итоговая сумма: {result_value:.2f} RUB\n")
                    else:
                        f.write(f"Итоговая сумма: {0:.2f} RUB\n")  # если результат не числовой
                    f.write("=" * 50 + "\n\n")

                reports_logger.info(f"Отчет сохранен в файл: {report_filename}")
            except IOError as e:
                reports_logger.error(f"Ошибка записи отчета: {str(e)}")

            return result

        return wrapper

    return decorator


@save_report_to_file()
def spending_by_category(df_data: pd.DataFrame, chosen_category: str, end_date: Optional[str] = None) -> str:
    """
    Считает сумму операций по указанной категории за последние 3 месяца.

    Args:
        df_data: DataFrame с колонками ["Категория", "Сумма операции", "Дата платежа", "Статус", "Валюта операции"]
        chosen_category: Категория для фильтрации
        end_date: Конечная дата в формате строки (если None - используется текущая дата)

    Returns:
        Сумма в рублях операций по категории за период
    """
    total_amount = 0.0
    try:
        end_date_obj = parse(end_date).date() if end_date else datetime.date.today()
        reports_logger.info(f"Конечная дата установлена: {end_date_obj}")
    except (ValueError, TypeError, KeyError) as e:
        end_date_obj = datetime.date.today()
        reports_logger.warning(f"Ошибка парсинга даты: {str(e)}. Использована текущая дата")

    start_date_obj = end_date_obj - relativedelta(months=3)
    reports_logger.info(f"Период анализа: с {start_date_obj} по {end_date_obj}")

    for _, row in df_data.iterrows():
        try:
            amount_date_obj = datetime.datetime.strptime(row["Дата платежа"], "%d.%m.%Y").date()
            amount = float(row["Сумма операции"])
            status = row["Статус"]
            currency = row["Валюта операции"]

            if currency != "RUB":
                amount = get_currency_rate(currency, row["Дата платежа"]) * amount
                reports_logger.debug(f"Конвертация валюты: {amount} {currency} -> RUB")

            if (
                row["Категория"] == chosen_category
                and start_date_obj <= amount_date_obj <= end_date_obj
                and amount < 0
                and status == "OK"
            ):
                total_amount += abs(amount)

        except (ValueError, TypeError, KeyError) as e:
            reports_logger.error(f"Ошибка обработки строки: {str(e)}")
            continue

    result = round(total_amount, 2)
    reports_logger.info(f"Итоговая сумма по категории '{chosen_category}': {result:.2f} RUB")
    return json.dumps(result, ensure_ascii=False, indent=4)
