import pytest
from src.constructor import Vacancy


@pytest.fixture
def sample_vacancies():
    return [
        Vacancy("Python Dev", "http://example.com", {"from": 100000}, "Python 3+"),
        Vacancy("Java Dev", "http://example.com", {"from": 90000}, "Java 11+"),
        Vacancy("Intern", "http://example.com", None, "No exp needed"),
    ]


@pytest.fixture
def sample_json_data():
    return [
        {
            "name": "Test",
            "salary": {"from": 50000, "currency": "RUB"},
            "alternate_url": "http://test.com",
            "snippet": {"requirement": "Python 3+"},
            "description": "Test description",
        }
    ]
