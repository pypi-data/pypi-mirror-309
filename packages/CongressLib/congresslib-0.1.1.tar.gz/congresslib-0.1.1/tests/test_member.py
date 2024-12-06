import pytest
from unittest.mock import patch
from congresslib.member import Member
from congresslib.main import PyCongress

@pytest.fixture
def client():
    """
    Fixture to create a Member client instance.
    """
    return PyCongress(apikey="test_api_key").member

@patch("requests.get")
def test_get_member_list(mock_get, client):
    """
    Test the get_member_list method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"members": [{"id": 1, "name": "Member 1"}]}

    response = client.get_member_list(limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["name"] == "Member 1"

@patch("requests.get")
def test_get_member(mock_get, client):
    """
    Test the get_member method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"member": {"id": "A0001", "name": "Member 1"}}

    response = client.get_member(id="A0001")
    assert isinstance(response, dict)
    assert response["id"] == "A0001"
    assert response["name"] == "Member 1"

@patch("requests.get")
def test_get_sponsored_legislation(mock_get, client):
    """
    Test the get_sponsored_legislation method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"sponsoredLegislation": [{"id": 1, "title": "Legislation 1"}]}

    response = client.get_sponsored_legislation(id="A0001", limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["title"] == "Legislation 1"

@patch("requests.get")
def test_get_cosponsored_legislation(mock_get, client):
    """
    Test the get_cosponsored_legislation method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"cosponsoredLegislation": [{"id": 1, "title": "Legislation 1"}]}

    response = client.get_cosponsored_legislation(id="A0001", limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["title"] == "Legislation 1"

@patch("requests.get")
def test_invalid_member_district(mock_get, client):
    """
    Test invalid district raises ValueError.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"members: []"}

    with pytest.raises(ValueError):
        client.get_member_list(state=None, district=1)
