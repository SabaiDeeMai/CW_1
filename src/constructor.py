from typing import Dict, List, Optional


class Vacancy:
    __slots__ = ("title", "url", "salary", "description")

    def __init__(self, title: str, url: str, salary: Optional[Dict], description: str):
        self.title = title or "Без названия"
        self.url = url or "#"
        self.salary = salary or {"from": None, "to": None, "currency": None}
        self.description = description or "Описание отсутствует"

    def __str__(self):
        salary_from = self.salary.get("from", "?")
        salary_to = self.salary.get("to", "?")
        return (
            f"{self.title}\n"
            f"Зарплата: {salary_from}-{salary_to} {self.salary.get('currency', '')}\n"
            f"Ссылка: {self.url}\n"
        )

    @classmethod
    def cast_to_object_list(cls, data: List[Dict]) -> List["Vacancy"]:
        return [
            cls(
                title=v.get("name"),
                url=v.get("alternate_url"),
                salary=v.get("salary"),
                description=v.get("snippet", {}).get("requirement", ""),
            )
            for v in data
        ]
