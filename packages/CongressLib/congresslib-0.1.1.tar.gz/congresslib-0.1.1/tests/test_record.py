import pytest
from unittest.mock import patch
from congresslib.record import Record
from congresslib.main import PyCongress

@pytest.fixture
def client():
    """
    Fixture to create a Record client instance.
    """
    return PyCongress(apikey="test_api_key").record

@patch("requests.get")
def test_get_record_list(mock_get, client):
    """
    Test the get_record_list method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"Results": [{"id": 1, "title": "Record 1"}]}

    response = client.get_record_list(year=2023, month=5, day=15, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["title"] == "Record 1"

@patch("requests.get")
def test_get_daily_record_list(mock_get, client):
    """
    Test the get_daily_record_list method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"dailyCongressionalRecord": [{"id": 1, "volume": "Volume 1"}]}

    response = client.get_daily_record_list(volume="1", limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["volume"] == "Volume 1"

@patch("requests.get")
def test_get_daily_record(mock_get, client):
    """
    Test the get_daily_record method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"issue": [{"id": 1, "title": "Daily Record 1"}]}

    response = client.get_daily_record(volume="1", issue="2", limit=1)
    assert isinstance(response, dict)
    assert response["id"] == 1
    assert response["title"] == "Daily Record 1"

@patch("requests.get")
def test_get_daily_record_articles(mock_get, client):
    """
    Test the get_daily_record_articles method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"articles": [{"id": 1, "title": "Article 1"}]}

    response = client.get_daily_record_articles(volume="1", issue="2", limit=1)
    assert isinstance(response, list)
    assert response[0]["id"] == 1
    assert response[0]["title"] == "Article 1"

@patch("requests.get")
def test_get_bound_record_list(mock_get, client):
    """
    Test the get_bound_record_list method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"boundCongressionalRecord": [{"id": 1, "title": "Bound Record 1"}]}

    response = client.get_bound_record_list(year=2023, month=5, day=15, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["title"] == "Bound Record 1"
