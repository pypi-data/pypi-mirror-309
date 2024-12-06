import pytest
from unittest.mock import patch
from congresslib.congress import Congress
from congresslib.main import PyCongress

@pytest.fixture
def client():
    """
    Fixture to create a Congress client instance.
    """
    return PyCongress(apikey="test_api_key").congress

@patch("requests.get")
def test_get_congress_list(mock_get, client):
    """
    Test the get_congress_list method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"congresses": [{"id": 1, "name": "Congress 1"}]}

    response = client.get_congress_list(limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["name"] == "Congress 1"

@patch("requests.get")
def test_get_congress(mock_get, client):
    """
    Test the get_congress method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"congress": {"id": 1, "name": "Congress 1"}}

    response = client.get_congress(congress=117)
    assert isinstance(response, dict)
    assert response["id"] == 1
    assert response["name"] == "Congress 1"

@patch("requests.get")
def test_get_current_congress(mock_get, client):
    """
    Test the get_current_congress method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"congress": {"id": 118, "name": "Current Congress"}}

    response = client.get_current_congress()
    assert isinstance(response, dict)
    assert response["id"] == 118
    assert response["name"] == "Current Congress"
