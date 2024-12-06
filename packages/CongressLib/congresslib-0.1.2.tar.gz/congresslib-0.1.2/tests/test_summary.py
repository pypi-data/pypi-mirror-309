import pytest
from unittest.mock import patch
from congresslib.summary import Summary
from congresslib.main import PyCongress

@pytest.fixture
def client():
    """
    Fixture to create a Summary client instance.
    """
    return PyCongress(apikey="test_api_key").summary

@patch("requests.get")
def test_get_summary_list(mock_get, client):
    """
    Test the get_summary_list method.
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"summaries": [{"id": 1, "title": "Summary 1"}]}

    response = client.get_summary_list(congress=117, type="hr", sort="asc", limit=1)
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]["id"] == 1
    assert response[0]["title"] == "Summary 1"

@patch("requests.get")
def test_get_summary_list_invalid_sort(mock_get, client):
    """
    Test the get_summary_list method with an invalid sort order.
    """
    with pytest.raises(ValueError, match="Invalid sort order"):
        client.get_summary_list(congress=117, type="hr", sort="invalid", limit=1)

@patch("requests.get")
def test_get_summary_list_invalid_type(mock_get, client):
    """
    Test the get_summary_list method with an invalid bill type.
    """
    with pytest.raises(ValueError, match="Invalid bill type"):
        client.get_summary_list(congress=117, type="invalid", sort="asc", limit=1)

@patch("requests.get")
def test_get_summary_list_missing_congress(mock_get, client):
    """
    Test the get_summary_list method with type specified but missing congress.
    """
    with pytest.raises(ValueError, match="'congres' must be specified when 'type' is provided"):
        client.get_summary_list(type="hr", sort="asc", limit=1)
