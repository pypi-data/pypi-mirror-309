import pytest
from unittest.mock import patch
from congresslib.communication import Communication
from congresslib.main import PyCongress

@pytest.fixture
def client():
    """
    Fixture to create a Communication client instance.
    """
    return PyCongress(apikey="test_api_key").communication

@patch("requests.get")
def test_get_communication_list(mock_get, client):
    """
    Test the get_communication_list method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"houseCommunications": [{"id": 1, "title": "Communication 1"}]}

    response = client.get_communication_list(chamber="house", limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["title"] == "Communication 1"

@patch("requests.get")
def test_get_communication(mock_get, client):
    """
    Test the get_communication method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"houseCommunication": {"id": 1, "title": "Communication 1"}}

    response = client.get_communication(chamber="house", congress=117, type="ec", number=1)
    assert isinstance(response, dict)
    assert response["id"] == 1
    assert response["title"] == "Communication 1"

@patch("requests.get")
def test_get_requirement_list(mock_get, client):
    """
    Test the get_requirement_list method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"houseRequirements": [{"id": 1, "title": "Requirement 1"}]}

    response = client.get_requirement_list(limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["title"] == "Requirement 1"

@patch("requests.get")
def test_get_requirement(mock_get, client):
    """
    Test the get_requirement method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"houseRequirements": {"id": 1, "title": "Requirement 1"}}

    response = client.get_requirement(number="1")
    assert isinstance(response, dict)
    assert response["id"] == 1
    assert response["title"] == "Requirement 1"

@patch("requests.get")
def test_get_requirement_communications(mock_get, client):
    """
    Test the get_requirement_communications method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"matchingCommunications": [{"id": 1, "title": "Communication 1"}]}

    response = client.get_requirement_communications(number="1", limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["title"] == "Communication 1"

@patch("requests.get")
def test_invalid_chamber_type(mock_get, client):
    """
    Test invalid chamber type raises ValueError.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"communications: []"}

    with pytest.raises(ValueError):
        client.get_communication_list(chamber="invalid")

@patch("requests.get")
def test_invalid_communication_type(mock_get, client):
    """
    Test invalid communication type raises ValueError.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"communication: []"}

    with pytest.raises(ValueError):
        client.get_communication(chamber="house", congress=117, type="invalid", number=1)
