from typing import List
from src.constructor import Vacancy


def filter_vacancies(vacancies: List[Vacancy], keywords: List[str]) -> List[Vacancy]:
    """Фильтрация вакансий по ключевым словам в названии и описании"""
    if not keywords or not vacancies:
        return vacancies

    filtered = []
    keywords_lower = [kw.lower() for kw in keywords if kw]

    for vacancy in vacancies:
        search_text = f"{vacancy.title} {vacancy.description}".lower()
        if all(kw in search_text for kw in keywords_lower):
            filtered.append(vacancy)
    return filtered


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортировка по зарплате (от высокой к низкой) с обработкой None"""

    def get_sort_key(v: Vacancy) -> tuple:
        salary = v.salary or {}
        salary_from = salary.get("from")
        salary_to = salary.get("to")

        return (
            0 if salary_from is not None else (1 if salary_to is not None else 2),
            -(salary_from or salary_to or 0),  # Убывание через минус
            v.title,  # Для стабильности
        )

    return sorted(vacancies, key=get_sort_key)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Получение топ-N вакансий с защитой от некорректных значений"""
    try:
        return vacancies[: max(0, int(top_n))]
    except (TypeError, ValueError):
        return []


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Выводит отформатированный список вакансий с цветовой разметкой"""
    if not vacancies:
        print("\n\033[91m✖ Вакансии не найдены\033[0m")
        print("\033[93mПопробуйте изменить параметры поиска\033[0m\n")
        return

    print(f"\n\033[92mНайдено вакансий: {len(vacancies)}\033[0m")
    for i, vac in enumerate(vacancies, 1):
        # Форматирование зарплаты
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
                    f"{currency}\033[0m"
                )

        # Вывод информации
        print(
            f"\n\033[1m{i}. {vac.title or 'Без названия'}\033[0m\n"
            f"{salary_info}"
            f"\n\033[36mОписание: {(vac.description or 'Нет описания')[:200]}"
            f"{'...' if len(vac.description or '') > 200 else ''}\033[0m\n"
            f"\033[95mСсылка: {vac.url or 'не указана'}\033[0m"
        )
    print()
