import pytest
from unittest.mock import patch
from congresslib.bill import Bill
from congresslib.main import PyCongress

@pytest.fixture
def client():
    """
    Fixture to create a Bill client instance.
    """
    return PyCongress(apikey="test_api_key").bill

@patch("requests.get")
def test_get_bill_list(mock_get, client):
    """
    Test the get_bill_list method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"bills": [{"id": 1}]}

    response = client.get_bill_list(limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1

@patch("requests.get")
def test_get_bill_list_invalid_type(mock_get, client):
    """
    Test get_bill_list with an invalid bill type.
    """
    with pytest.raises(ValueError):
        client.get_bill_list(type="invalid")

@patch("requests.get")
def test_get_bill(mock_get, client):
    """
    Test the get_bill method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"bill": {"id": 1, "title": "Test Bill"}}

    response = client.get_bill(congress=117, type="hr", number=1)
    assert isinstance(response, dict)
    assert response["id"] == 1
    assert response["title"] == "Test Bill"

@patch("requests.get")
def test_get_bill_invalid_type(mock_get, client):
    """
    Test get_bill with an invalid bill type.
    """
    with pytest.raises(ValueError):
        client.get_bill(congress=117, type="invalid", number=1)

@patch("requests.get")
def test_get_bill_actions(mock_get, client):
    """
    Test the get_bill_actions method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"actions": [{"id": 1, "description": "Action 1"}]}

    response = client.get_bill_actions(congress=117, type="hr", number=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["description"] == "Action 1"

@patch("requests.get")
def test_get_bill_amendments(mock_get, client):
    """
    Test the get_bill_amendments method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"amendments": [{"id": 1, "description": "Amendment 1"}]}

    response = client.get_bill_amendments(congress=117, type="hr", number=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["description"] == "Amendment 1"

@patch("requests.get")
def test_get_bill_committees(mock_get, client):
    """
    Test the get_bill_committees method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"committees": [{"id": 1, "name": "Committee 1"}]}

    response = client.get_bill_committees(congress=117, type="hr", number=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["name"] == "Committee 1"

@patch("requests.get")
def test_get_bill_cosponsors(mock_get, client):
    """
    Test the get_bill_cosponsors method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"cosponsors": [{"id": 1, "name": "Sponsor 1"}]}

    response = client.get_bill_cosponsors(congress=117, type="hr", number=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["name"] == "Sponsor 1"

@patch("requests.get")
def test_get_bill_relatedbills(mock_get, client):
    """
    Test the get_bill_relatedbills method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"relatedBills": [{"id": 1, "title": "Related Bill 1"}]}

    response = client.get_bill_relatedbills(congress=117, type="hr", number=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["title"] == "Related Bill 1"

@patch("requests.get")
def test_get_bill_subjects(mock_get, client):
    """
    Test the get_bill_subjects method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"subjects": [{"id": 1, "name": "Subject 1"}]}

    response = client.get_bill_subjects(congress=117, type="hr", number=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["name"] == "Subject 1"

@patch("requests.get")
def test_get_bill_summaries(mock_get, client):
    """
    Test the get_bill_summaries method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"summaries": [{"id": 1, "text": "Summary 1"}]}

    response = client.get_bill_summaries(congress=117, type="hr", number=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["text"] == "Summary 1"

@patch("requests.get")
def test_get_bill_text(mock_get, client):
    """
    Test the get_bill_text method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"textVersions": [{"id": 1, "text": "Text Version 1"}]}

    response = client.get_bill_text(congress=117, type="hr", number=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["text"] == "Text Version 1"

@patch("requests.get")
def test_get_bill_titles(mock_get, client):
    """
    Test the get_bill_titles method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"titles": [{"id": 1, "title": "Title 1"}]}

    response = client.get_bill_titles(congress=117, type="hr", number=1, limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["title"] == "Title 1"
