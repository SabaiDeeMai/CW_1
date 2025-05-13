from unittest.mock import patch, MagicMock
import builtins
import src.main as main_module


@patch("src.main.read_excel_file")
@patch("src.main.read_excel_file_to_df")
@patch("src.main.generate_finance_report")
@patch("src.main.get_search_by_mobile_numbers")
@patch("src.main.spending_by_category")
@patch.object(builtins, "input", side_effect=["Транспорт", "01.01.2024"])
@patch.object(builtins, "print")
def test_main_workflow(mock_print, mock_input, mock_spending, mock_search, mock_report, mock_read_df, mock_read_excel):
    # Настраиваем возвращаемые значения
    mock_read_excel.return_value = {
        "data": [{"Номер карты": "1234567890123456", "Сумма операции": -100, "Статус": "OK", "Валюта операции": "RUB"}]
    }
    mock_read_df.return_value = "mocked_df"
    mock_report.return_value = "Mocked Report"
    mock_search.return_value = "Mocked Phone Search"
    mock_spending.return_value = "Mocked Category Spending"

    # Запуск main()
    main_module.main()

    # Проверка, что функции вызывались с нужными параметрами
    mock_input.assert_any_call("Напишите название категории\n")
    mock_input.assert_any_call(
        "Напишите конечную дату поиска\n"
        "Поиск будет в диапазоне 3 месяцев\n"
        "Если дата неверна или не указана, то отсчет будет до сегодняшней даты\n"
    )

    mock_report.assert_called_once()
    mock_search.assert_called_once()
    mock_spending.assert_called_once_with("mocked_df", "Транспорт", "01.01.2024")
    mock_print.assert_any_call("Mocked Report", "Mocked Phone Search", "Mocked Category Spending")
