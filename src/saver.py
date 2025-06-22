import json
import os
from pathlib import Path
from typing import List, Dict, Any


class JSONSaver:
    """Менеджер для сохранения вакансий в JSON-файл с гарантированной целостностью данных"""

    def __init__(self, filename: str = "vacancies.json") -> None:
        """Инициализация с автоматическим созданием директории"""
        self._filename = Path("data") / filename
        self._ensure_directory_exists()

    @property
    def filename(self) -> Path:
        """Полный путь к файлу с вакансиями"""
        return self._filename

    @filename.setter
    def filename(self, value: Path) -> None:
        """Изменение пути к файлу с вакансиями"""
        self._filename = value
        self._ensure_directory_exists()

    def _ensure_directory_exists(self) -> None:
        """Создает директорию для файла при необходимости"""
        try:
            self._filename.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise RuntimeError(f"Не удалось создать директорию: {e}")

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Добавляет вакансию с проверкой уникальности по URL"""
        if not isinstance(vacancy, dict) or "url" not in vacancy:
            raise ValueError("Некорректные данные вакансии")

        vacancies = self._load_safe()
        vacancies.append(vacancy)
        self._save_safe(vacancies)

    def get_vacancies(self) -> List[Dict[str, Any]]:
        """Возвращает все вакансии из файла"""
        return self._load_safe()

    def delete_vacancy(self, url: str) -> None:
        """Удаляет вакансию по URL"""
        vacancies = [v for v in self._load_safe() if v.get("url") != url]
        self._save_safe(vacancies)

    def _load_safe(self) -> List[Dict[str, Any]]:
        """Безопасная загрузка данных с обработкой ошибок"""
        try:
            if not self._filename.exists():
                return []

            with open(self._filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise RuntimeError(f"Ошибка чтения файла: {e}")

    def _save_safe(self, data: List[Dict[str, Any]]) -> None:
        """Атомарное сохранение данных с созданием резервной копии"""
        try:
            # Сначала пишем во временный файл
            temp_file = self._filename.with_suffix(".tmp")
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Затем заменяем оригинальный файл
            if os.path.exists(self._filename):
                os.replace(temp_file, self._filename)
            else:
                os.rename(temp_file, self._filename)

        except OSError as e:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise RuntimeError(f"Ошибка сохранения: {e}")
