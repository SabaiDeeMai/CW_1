from src.utils import read_excel_file, read_excel_file_to_df
from src.views import generate_finance_report
from src.services import get_search_by_mobile_numbers
from src.reports import spending_by_category


def main():
    excel_file = "../data/operations.xlsx"
    excel_data = read_excel_file(excel_file)
    df_from_excel_file = read_excel_file_to_df(excel_file)
    if not excel_data:
        print("\nНет данных для обработки!\n")
    else:
        task_1 = generate_finance_report(excel_data)
        print(task_1)
        task_2 = get_search_by_mobile_numbers(excel_data)
        print(task_2)
        print("\nДанные успешно обработаны!\n")
        category = input("Напишите название категории\n")
        end_date = input(
            "Напишите конечную дату поиска\n"
            "Поиск будет в диапазоне 3 месяцев\n"
            "Если дата неверна или не указана, то отсчет будет до сегодняшней даты\n"
        )
        task_3 = spending_by_category(df_from_excel_file, category, end_date)
        print(task_3)


if __name__ == "__main__":
    main()
