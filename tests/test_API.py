from unittest.mock import Mock, patch
from src.API import HeadHunterAPI
import pytest


@patch("requests.get")
def test_get_vacancies(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"name": "Test"}]}
    mock_get.return_value = mock_response

    api = HeadHunterAPI()
    vacancies = api.get_vacancies("python")

    assert len(vacancies) == 1
    assert vacancies[0]["name"] == "Test"
