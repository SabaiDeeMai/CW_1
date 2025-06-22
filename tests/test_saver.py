import os
import json
import pytest
from src.saver import JSONSaver


def test_file_operations(tmp_path):
    """Интеграционный тест работы с файлами: создание, чтение, удаление"""
    # 1. Настройка тестового окружения
    test_filename = "test_vacancies.json"
    test_dir = tmp_path / "data"
    test_dir.mkdir()

    # 2. Инициализация с явным указанием пути
    saver = JSONSaver(filename=test_filename)
    saver.filename = test_dir / test_filename  # Переопределяем путь для теста

    # 3. Тест добавления
    test_data = {
        "title": "Python Developer",
        "url": "http://test.com",
        "salary": {"from": 100000},
        "description": "Test description",
    }

    # Первое добавление
    saver.add_vacancy(test_data)
    assert os.path.exists(saver.filename), "Файл должен быть создан после добавления"

    # 4. Проверка содержимого
    with open(saver.filename, "r", encoding="utf-8") as f:
        content = json.load(f)
        assert len(content) == 1, "Должна быть ровно одна вакансия"
        assert content[0]["title"] == test_data["title"]

    # 5. Тест удаления
    saver.delete_vacancy(test_data["url"])
    assert os.path.exists(saver.filename), "Файл должен остаться после удаления"

    with open(saver.filename, "r", encoding="utf-8") as f:
        assert json.load(f) == [], "Файл должен быть пустым после удаления"
