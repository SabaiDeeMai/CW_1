import pytest
from src.constructor import Vacancy


def test_vacancy_creation():
    v = Vacancy("Python Dev", "http://test.com", {"from": 100000}, "Опыт 3+ года")
    assert v.title == "Python Dev"
    assert v.salary["from"] == 100000


def test_default_values():
    v = Vacancy(None, None, None, None)
    assert v.title == "Без названия"
    assert v.url == "#"
    assert v.description == "Нет описания"


def test_cast_to_object_list():
    test_data = [
        {
            "name": "Test",
            "alternate_url": "http://test.com",
            "salary": {"from": 50000},
            "snippet": {"requirement": "Python"},
        }
    ]

    vacancies = Vacancy.cast_to_object_list(test_data)
    assert len(vacancies) == 1
    assert vacancies[0].title == "Test"


def test_invalid_salary_data():
    v = Vacancy("Test", "url", {"invalid": "data"}, "Desc")
    assert v.salary == {"invalid": "data"}
