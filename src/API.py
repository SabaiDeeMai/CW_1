from abc import ABC, abstractmethod
import requests
from typing import List, Dict


class JobAPI(ABC):
    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict]:
        pass


class HeadHunterAPI(JobAPI):
    __BASE_URL = "https://api.hh.ru/vacancies"

    def get_vacancies(self, keyword: str) -> List[Dict]:
        params = {"text": keyword, "per_page": 100}
        response = requests.get(self.__BASE_URL, params=params)
        response.raise_for_status()
        return response.json().get("items", [])
