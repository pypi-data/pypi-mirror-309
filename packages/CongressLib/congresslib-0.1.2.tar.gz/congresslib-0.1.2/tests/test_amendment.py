import pytest
from unittest.mock import patch
from congresslib.amendment import Amendment
from congresslib.main import PyCongress

@pytest.fixture
def client():
    """
    Fixture to create an Amendment client instance.
    """
    return PyCongress(apikey="test_api_key").amendment

@patch("requests.get")
def test_get_amendment_list(mock_get, client):
    """
    Test the get_amendment_list method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"amendments": [{"id": 1}]}

    response = client.get_amendment_list(limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1

@patch("requests.get")
def test_get_amendment(mock_get, client):
    """
    Test the get_amendment method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"amendment": {"id": 1, "title": "Test Amendment"}}

    response = client.get_amendment(congress=117, type="h", number=1)
    assert isinstance(response, dict)
    assert response["id"] == 1
    assert response["title"] == "Test Amendment"

@patch("requests.get")
def test_get_amendment_actions(mock_get, client):
    """
    Test the get_amendment_actions method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"actions": [{"id": 1, "description": "Action 1"}]}

    response = client.get_amendment_actions(congress=117, type="h", number=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["description"] == "Action 1"

@patch("requests.get")
def test_get_amendment_cosponsors(mock_get, client):
    """
    Test the get_amendment_cosponsors method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"cosponsors": [{"id": 1, "name": "Sponsor 1"}]}

    response = client.get_amendment_cosponsors(congress=117, type="h", number=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["name"] == "Sponsor 1"

@patch("requests.get")
def test_get_amendment_amendments(mock_get, client):
    """
    Test the get_amendment_amendments method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"amendments": [{"id": 1, "description": "Amendment 1"}]}

    response = client.get_amendment_amendments(congress=117, type="h", number=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["description"] == "Amendment 1"

@patch("requests.get")
def test_get_amendment_text(mock_get, client):
    """
    Test the get_amendment_text method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"textVersions": [{"id": 1, "text": "Text Version 1"}]}

    response = client.get_amendment_text(congress=117, type="h", number=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["text"] == "Text Version 1"

@patch("requests.get")
def test_invalid_amendment_type(mock_get, client):
    """
    Test invalid amendment type raises ValueError.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"amendments: []"}

    with pytest.raises(ValueError):
        client.get_amendment_list(congress=117, type="invalid")

@patch("requests.get")
def test_invalid_amendment_text_congress(mock_get, client):
    """
    Test invalid congress value for get_amendment_text.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"text: []"}

    with pytest.raises(ValueError):
        client.get_amendment_text(congress=116, type="h", number=1)
