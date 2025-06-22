from __future__ import annotations
from typing import Optional, Dict, List


class Vacancy:
    """Класс для представления вакансии"""

    def __init__(
        self,
        title: Optional[str],
        url: Optional[str],
        salary: Optional[Dict[str, Optional[int]]],
        description: Optional[str],
    ):
        """
        Args:
            title: Название вакансии
            url: Ссылка на вакансию
            salary: Зарплата (from, to, currency)
            description: Описание вакансии
        """
        self.title = title if title is not None else "Без названия"
        self.url = url if url is not None else "#"
        self.salary = (
            salary
            if salary is not None
            else {"from": None, "to": None, "currency": None}
        )
        self.description = description if description is not None else "Нет описания"

    @classmethod
    def cast_to_object_list(cls, vacancies_json: List[Dict]) -> List["Vacancy"]:
        """Преобразует JSON-данные в список объектов Vacancy

        Args:
            vacancies_json: Список вакансий в формате JSON от API HH.ru

        Returns:
            Список объектов Vacancy
        """
        vacancies = []
        for v in vacancies_json:
            try:
                salary = v.get("salary")
                description = (
                    v.get("snippet", {}).get("requirement")
                    or v.get("description")
                    or "Нет описания"
                )

                vacancies.append(
                    cls(
                        title=v.get("name"),
                        url=v.get("alternate_url"),
                        salary=salary,
                        description=description,
                    )
                )
            except Exception as e:
                print(f"Ошибка при создании вакансии: {e}")
                continue
        return vacancies
