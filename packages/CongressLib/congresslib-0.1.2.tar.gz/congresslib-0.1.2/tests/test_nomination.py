import pytest
from unittest.mock import patch
from congresslib.nomination import Nomination
from congresslib.main import PyCongress

@pytest.fixture
def client():
    """
    Fixture to create a Nomination client instance.
    """
    return PyCongress(apikey="test_api_key").nomination

@patch("requests.get")
def test_get_nomination_list(mock_get, client):
    """
    Test the get_nomination_list method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"nominations": [{"id": 1, "name": "Nomination 1"}]}

    response = client.get_nomination_list(limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["name"] == "Nomination 1"

@patch("requests.get")
def test_get_nomination(mock_get, client):
    """
    Test the get_nomination method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"nomination": {"id": 1, "name": "Nomination 1"}}

    response = client.get_nomination(congress=117, number=1)
    assert isinstance(response, dict)
    assert response["id"] == 1
    assert response["name"] == "Nomination 1"

@patch("requests.get")
def test_get_nominees(mock_get, client):
    """
    Test the get_nominees method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"nominees": [{"id": 1, "name": "Nominee 1"}]}

    response = client.get_nominees(congress=117, number=1, ordinal=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["name"] == "Nominee 1"

@patch("requests.get")
def test_get_nomination_actions(mock_get, client):
    """
    Test the get_nomination_actions method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"actions": [{"id": 1, "description": "Action 1"}]}

    response = client.get_nomination_actions(congress=117, number=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["description"] == "Action 1"

@patch("requests.get")
def test_get_nomination_committees(mock_get, client):
    """
    Test the get_nomination_committees method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"committees": [{"id": 1, "name": "Committee 1"}]}

    response = client.get_nomination_committeees(congress=117, number=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["name"] == "Committee 1"

@patch("requests.get")
def test_get_nomination_hearings(mock_get, client):
    """
    Test the get_nomination_hearings method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"hearings": [{"id": 1, "title": "Hearing 1"}]}

    response = client.get_nomination_hearings(congress=117, number=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["title"] == "Hearing 1"
