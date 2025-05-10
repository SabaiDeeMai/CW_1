from src.utils import read_excel_file
from src.views import generate_finance_report


def main():
    excel_file = "../data/operations.xlsx"
    excel_data = read_excel_file(excel_file)
    if not excel_data:
        print("\nНет данных для обработки!\n")
    else:
        print("\nДанные успешно обработаны!\n")
        test = generate_finance_report(excel_data)
        print(test)


if __name__ == "__main__":
    main()
