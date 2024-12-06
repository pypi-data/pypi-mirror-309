import pytest
from unittest.mock import patch
from congresslib.treaty import Treaty
from congresslib.main import PyCongress

@pytest.fixture
def client():
    """
    Fixture to create a Treaty client instance.
    """
    return PyCongress(apikey="test_api_key").treaty

@patch("requests.get")
def test_get_treaty_list(mock_get, client):
    """
    Test the get_treaty_list method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"treaties": [{"id": 1, "title": "Treaty 1"}]}

    response = client.get_treaty_list(congress=117, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["title"] == "Treaty 1"

@patch("requests.get")
def test_get_treaty(mock_get, client):
    """
    Test the get_treaty method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"treaty": {"id": 1, "title": "Treaty 1"}}

    response = client.get_treaty(congress=117, number=1)
    assert isinstance(response, dict)
    assert response["id"] == 1
    assert response["title"] == "Treaty 1"

@patch("requests.get")
def test_get_treaty_with_suffix(mock_get, client):
    """
    Test the get_treaty method with a suffix.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"treaty": {"id": 1, "title": "Treaty 1"}}

    response = client.get_treaty(congress=117, number=1, suffix="A")
    assert isinstance(response, dict)
    assert response["id"] == 1
    assert response["title"] == "Treaty 1"

@patch("requests.get")
def test_get_treaty_actions(mock_get, client):
    """
    Test the get_treaty_actions method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"actions": [{"id": 1, "description": "Action 1"}]}

    response = client.get_treaty_actions(congress=117, number=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["description"] == "Action 1"

@patch("requests.get")
def test_get_treaty_actions_with_suffix(mock_get, client):
    """
    Test the get_treaty_actions method with a suffix.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"actions": [{"id": 1, "description": "Action 1"}]}

    response = client.get_treaty_actions(congress=117, number=1, suffix="A", limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["description"] == "Action 1"

@patch("requests.get")
def test_get_treaty_committees(mock_get, client):
    """
    Test the get_treaty_committees method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"treatyCommittees": [{"id": 1, "name": "Committee 1"}]}

    response = client.get_treaty_committees(congress=117, number=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["name"] == "Committee 1"
