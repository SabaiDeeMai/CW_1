import pytest
from src.filter import filter_vacancies, sort_vacancies, get_top_vacancies
from src.constructor import Vacancy  # Явный импорт класса


@pytest.fixture
def sample_vacancies():
    """Фикстура с тестовыми вакансиями"""
    return [
        Vacancy(
            "Python Developer", "http://python.dev", {"from": 100000}, "Python 3.8+"
        ),
        Vacancy("Java Developer", "http://java.dev", {"from": 90000}, "Java 11+"),
        Vacancy("C++ Engineer", "http://cpp.dev", {"from": 120000}, "C++17/Boost"),
        Vacancy("Intern", "http://intern.dev", None, "No experience required"),
    ]


def test_filter_by_keyword(sample_vacancies):
    """Тест фильтрации по ключевому слову"""
    filtered = filter_vacancies(sample_vacancies, ["python"])
    assert len(filtered) == 1
    assert filtered[0].title == "Python Developer"


def test_filter_multiple_keywords(sample_vacancies):
    """Тест фильтрации по нескольким ключевым словам"""
    filtered = filter_vacancies(sample_vacancies, ["java", "11"])
    assert len(filtered) == 1
    assert filtered[0].title == "Java Developer"


def test_filter_special_chars(sample_vacancies):
    """Тест фильтрации с спецсимволами"""
    filtered = filter_vacancies(sample_vacancies, ["c++"])
    assert len(filtered) == 1
    assert filtered[0].title == "C++ Engineer"


def test_filter_case_insensitive(sample_vacancies):
    """Тест регистронезависимой фильтрации"""
    filtered = filter_vacancies(sample_vacancies, ["PYTHON"])
    assert len(filtered) == 1
    assert filtered[0].title == "Python Developer"


def test_filter_empty_result(sample_vacancies):
    """Тест пустого результата фильтрации"""
    filtered = filter_vacancies(sample_vacancies, ["ruby"])
    assert len(filtered) == 0


def test_sort_vacancies(sample_vacancies):
    """Тест сортировки по зарплате"""
    sorted_vacancies = sort_vacancies(sample_vacancies)
    assert sorted_vacancies[0].title == "C++ Engineer"
    assert sorted_vacancies[-1].title == "Intern"


def test_sort_vacancies(sample_vacancies):
    """Тест сортировки с вакансиями без зарплаты"""
    sorted_vacs = sort_vacancies(sample_vacancies)

    # Проверяем порядок:
    assert sorted_vacs[0].title == "C++ Engineer"  # 120000
    assert sorted_vacs[1].title == "Python Developer"  # 100000
    assert sorted_vacs[2].title == "Java Developer"  # 90000
    assert sorted_vacs[3].title == "Intern"  # Нет зарплаты

    # Проверяем что None не вызывает ошибок
    all_none = [Vacancy("NoSalary", "", None, "")]
    assert sort_vacancies(all_none)[0].title == "NoSalary"


def test_get_top_vacancies(sample_vacancies):
    """Тест получения топ-N с проверкой на некорректные значения"""
    sorted_vacs = sort_vacancies(sample_vacancies)

    # Нормальный случай
    top = get_top_vacancies(sorted_vacs, 2)
    assert len(top) == 2
    assert top[0].title == "C++ Engineer"

    # Крайние случаи
    assert len(get_top_vacancies([], 5)) == 0
    assert len(get_top_vacancies(sorted_vacs, -1)) == 0
    assert len(get_top_vacancies(sorted_vacs, "invalid")) == 0
