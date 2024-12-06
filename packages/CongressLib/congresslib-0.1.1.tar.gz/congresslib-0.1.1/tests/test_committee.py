import pytest
from unittest.mock import patch
from congresslib.committee import Committee
from congresslib.main import PyCongress

@pytest.fixture
def client():
    """
    Fixture to create a Committee client instance.
    """
    return PyCongress(apikey="test_api_key").committee

@patch("requests.get")
def test_get_committee_list(mock_get, client):
    """
    Test the get_committee_list method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"committees": [{"id": 1, "name": "Committee 1"}]}

    response = client.get_committee_list(limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["name"] == "Committee 1"

@patch("requests.get")
def test_get_committee(mock_get, client):
    """
    Test the get_committee method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"committee": {"id": 1, "name": "Committee 1"}}

    response = client.get_committee(chamber="house", code="HSAG")
    assert isinstance(response, dict)
    assert response["id"] == 1
    assert response["name"] == "Committee 1"

@patch("requests.get")
def test_get_committee_bills(mock_get, client):
    """
    Test the get_committee_bills method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"committee-bills": {"bills": [{"id": 1, "title": "Bill 1"}]}}

    response = client.get_committee_bills(chamber="house", code="HSAG", limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["title"] == "Bill 1"

@patch("requests.get")
def test_get_committee_reports(mock_get, client):
    """
    Test the get_committee_reports method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"reports": [{"id": 1, "title": "Report 1"}]}

    response = client.get_committee_reports(chamber="house", code="HSAG", limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["title"] == "Report 1"

@patch("requests.get")
def test_get_committee_nominations(mock_get, client):
    """
    Test the get_committee_nominations method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"nominations": [{"id": 1, "name": "Nomination 1"}]}

    response = client.get_committee_nominations(chamber="house", code="HSAG", limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["name"] == "Nomination 1"

@patch("requests.get")
def test_get_committee_communications(mock_get, client):
    """
    Test the get_committee_communications method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"houseCommunications": [{"id": 1, "title": "Communication 1"}]}

    response = client.get_committee_communications(chamber="house", code="HSAG", limit=1)
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
    mock_get.return_value.json.return_value = {"committees: []"}

    with pytest.raises(ValueError):
        client.get_committee_list(chamber="invalid")

@patch("requests.get")
def test_get_report_list(mock_get, client):
    """
    Test the get_report_list method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"reports": [{"id": 1, "title": "Report 1"}]}

    response = client.get_report_list(congress=117, type="h", limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["title"] == "Report 1"

@patch("requests.get")
def test_get_report(mock_get, client):
    """
    Test the get_report method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"committeeReports": [{"id": 1, "title": "Report 1"}]}

    response = client.get_report(congress=117, type="h", id=1)
    assert isinstance(response, dict)
    assert response["id"] == 1
    assert response["title"] == "Report 1"

@patch("requests.get")
def test_get_print_list(mock_get, client):
    """
    Test the get_print_list method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"committeePrints": [{"id": 1, "title": "Print 1"}]}

    response = client.get_print_list(congress=117, chamber="house", limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["title"] == "Print 1"

@patch("requests.get")
def test_get_meeting_list(mock_get, client):
    """
    Test the get_meeting_list method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"committeeMeetings": [{"id": 1, "name": "Meeting 1"}]}

    response = client.get_meeting_list(congress=117, chamber="house", limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["name"] == "Meeting 1"

@patch("requests.get")
def test_get_hearing_list(mock_get, client):
    """
    Test the get_hearing_list method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"hearings": [{"id": 1, "title": "Hearing 1"}]}

    response = client.get_hearing_list(congress=117, chamber="house", limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["title"] == "Hearing 1"
