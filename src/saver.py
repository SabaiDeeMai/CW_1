import json
from pathlib import Path
from typing import List, Dict, Any, Union
import logging


class JSONSaver:
    def __init__(self, filename: str = "vacancies.json"):
        self.filename = Path("data") / filename
        self.filename.parent.mkdir(exist_ok=True)
        logging.basicConfig(level=logging.INFO)

    def add_vacancy(self, vacancy: Any) -> None:
        """Безопасное добавление вакансии в файл"""
        try:
            data = self._load_data()

            if not isinstance(data, list):
                logging.warning("Invalid data format, recreating file")
                data = []

            vacancy_data = {
                "title": getattr(vacancy, "title", ""),
                "url": getattr(vacancy, "url", ""),
                "salary": getattr(vacancy, "salary", {}),
                "description": getattr(vacancy, "description", ""),
            }

            # Проверка на дубликаты
            if not self._is_duplicate(data, vacancy_data):
                data.append(vacancy_data)
                self._save_data(data)

        except Exception as e:
            logging.error(f"Error adding vacancy: {e}")

    def _is_duplicate(self, data: List[Dict], new_vacancy: Dict) -> bool:
        """Проверка на дубликаты вакансий"""
        if not isinstance(data, list):
            return False

        return any(
            isinstance(v, dict) and v.get("url") == new_vacancy["url"] for v in data
        )

    def _load_data(self) -> Union[List[Dict], List]:
        """Безопасная загрузка данных из файла"""
        try:
            if not self.filename.exists():
                return []

            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []

        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            logging.warning(f"Error loading JSON: {e}")
            return []
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return []

    def _save_data(self, data: List[Dict]) -> None:
        """Безопасное сохранение данных в файл"""
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error saving data: {e}")

    def get_vacancies(self) -> List[Dict]:
        """Получение всех вакансий"""
        return self._load_data()

    def delete_vacancy(self, url: str) -> None:
        """Удаление вакансии по URL"""
        try:
            data = self._load_data()
            if isinstance(data, list):
                new_data = [
                    v for v in data if isinstance(v, dict) and v.get("url") != url
                ]
                self._save_data(new_data)
        except Exception as e:
            logging.error(f"Error deleting vacancy: {e}")
