from src.API import HeadHunterAPI
from src.constructor import Vacancy
from src.filter import (
    filter_vacancies,
    sort_vacancies,
    get_top_vacancies,
    print_vacancies,
)
from src.saver import JSONSaver


def get_valid_number_input(prompt: str, default: int = 5) -> int:
    """Безопасный ввод числа с обработкой ошибок"""
    while True:
        try:
            user_input = input(prompt)
            if not user_input:  # Если просто нажали Enter
                return default
            return max(1, int(user_input))  # Преобразуем в число ≥1
        except ValueError:
            print("\033[91mОшибка: Введите целое число\033[0m")
            print(f"\033[93mИспользуется значение по умолчанию ({default})\033[0m")
            return default


def user_interaction():
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    # Защищенный ввод параметров
    search_query = input("Введите поисковый запрос: ").strip()
    top_n = get_valid_number_input(
        "Введите количество вакансий для вывода в топ N [по умолчанию 5]: ", 5
    )
    filter_word = input(
        "Введите ключевое слово для фильтрации (или Enter чтобы пропустить): "
    ).strip()

    # Получение и обработка вакансий
    hh_vacancies = hh_api.get_vacancies(search_query or "Python")  # Если пустой запрос
    try:
        vacancies = Vacancy.cast_to_object_list(hh_vacancies)
    except Exception as e:
        print(f"Ошибка обработки данных: {e}")
        vacancies = []

    # Фильтрация и вывод
    filtered = filter_vacancies(vacancies, [filter_word] if filter_word else [])
    sorted_vacs = sort_vacancies(filtered)
    top_vacancies = get_top_vacancies(sorted_vacs, top_n)

    # Сохранение и вывод
    for vac in top_vacancies:
        json_saver.add_vacancy(
            {
                "title": vac.title,
                "url": vac.url,
                "salary": vac.salary,
                "description": vac.description,
            }
        )
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
