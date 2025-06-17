from typing import List, Union
from src.constructor import Vacancy
import re


def validate_input_number(input_str: str, default: int = 5) -> int:
    """Проверка что введено число, а не строка"""
    try:
        num = int(input_str)
        return num if num > 0 else default
    except (ValueError, TypeError):
        return default


def filter_vacancies(
    vacancies: List[Vacancy], keywords: Union[str, List[str]]
) -> List[Vacancy]:
    """
    Улучшенная фильтрация с обработкой разных форматов ввода:
    - Принимает как строку, так и список ключевых слов
    - Автоматическая очистка от лишних пробелов
    - Защита от пустого ввода
    """
    if not vacancies:
        return []

    # Нормализация входных данных
    if isinstance(keywords, str):
        keywords = [kw.strip() for kw in keywords.split() if kw.strip()]
    elif not isinstance(keywords, list):
        return vacancies

    if not keywords:
        return vacancies

    filtered = []
    keywords = [re.sub(r"[^\w\s]", "", kw.lower()) for kw in keywords if kw]

    for vacancy in vacancies:
        try:
            search_text = " ".join(
                [
                    vacancy.title or "",
                    vacancy.description or "",
                    str(vacancy.salary.get("from", "")) if vacancy.salary else "",
                    str(vacancy.salary.get("to", "")) if vacancy.salary else "",
                ]
            ).lower()

            if any(
                re.search(rf"\b{re.escape(keyword)}", search_text)
                for keyword in keywords
            ):
                filtered.append(vacancy)
        except Exception:
            continue

    return filtered


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Надежная сортировка с обработкой None-значений"""

    def get_sort_key(v: Vacancy) -> tuple:
        salary = v.salary or {}
        return (
            0 if salary.get("from") is None else 1,
            salary.get("from", 0) or 0,
            salary.get("to", 0) or 0,
        )

    return sorted(vacancies, key=get_sort_key, reverse=True)


def get_top_vacancies(
    vacancies: List[Vacancy], top_n: Union[str, int]
) -> List[Vacancy]:
    """Безопасное получение N вакансий с проверкой ввода"""
    num = validate_input_number(top_n) if isinstance(top_n, str) else max(1, int(top_n))
    return vacancies[:num]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Улучшенный вывод с цветовой маркировкой и проверкой данных"""
    if not vacancies:
        print("\n\033[91m✖ Вакансии не найдены\033[0m")
        print("\033[93mПопробуйте изменить параметры поиска\033[0m\n")
        return

    print(f"\n\033[92mНайдено вакансий: {len(vacancies)}\033[0m")
    for i, vac in enumerate(vacancies, 1):
        salary_info = ""
        if vac.salary:
            from_sal = vac.salary.get("from", "?")
            to_sal = vac.salary.get("to", "?")
            currency = vac.salary.get("currency", "")

            if from_sal or to_sal:
                salary_info = (
                    f"\033[94mЗарплата: "
                    f"{from_sal if from_sal != '?' else 'не указана'}"
                    f"{f'-{to_sal}' if to_sal != '?' else ''} "
                    f"{currency if currency else ''}\033[0m"
                )

        print(
            f"\n\033[1m{i}. {vac.title or 'Без названия'}\033[0m\n"
            f"{salary_info}"
            f"\n\033[36mОписание: {(vac.description or 'Нет описания')[:200]}"
            f"{'...' if len(vac.description or '') > 200 else ''}\033[0m\n"
            f"\033[95mСсылка: {vac.url or 'не указана'}\033[0m"
        )
    print()
