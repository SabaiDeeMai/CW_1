from abc import abstractmethod


class Vacancy:

    profession: str = ""
    url: str = ""
    salary: str = ""
    requirements: str = ""

    def __init__(self, name: str, url: str, salary: int, employer: str):
        self.name = _validate_name(name)
        ...

    def _validate_name(self, name):
        if not isinstance(name, str):
            raise ValueError("Название вакансии должно быть строкой.")
        return name

    @classmethod
    def cast_to_object_list(cls, hh_vacancies):
        pass

    @abstractmethod
    def load_vacancies(self, keyword):
        """Создаем абстрактный метод для получения вакансий по ключевому слову"""
        pass
