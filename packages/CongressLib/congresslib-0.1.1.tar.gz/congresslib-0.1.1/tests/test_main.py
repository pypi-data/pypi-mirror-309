import pytest
from congresslib.main import PyCongress
from congresslib.amendment import Amendment
from congresslib.bill import Bill
from congresslib.committee import Committee
from congresslib.communication import Communication
from congresslib.congress import Congress
from congresslib.member import Member
from congresslib.nomination import Nomination
from congresslib.record import Record
from congresslib.summary import Summary
from congresslib.treaty import Treaty

@pytest.fixture
def client():
    """
    Fixture to create a PyCongress client instance.
    """
    return PyCongress(apikey="test_api_key")

def test_pycongress_initialization(client):
    """
    Test that the PyCongress client initializes correctly with the given API key.
    """
    assert client.apikey == "test_api_key"
    assert client.base_url == "https://api.congress.gov/v3/"

def test_submodule_initialization(client):
    """
    Test that all submodules of PyCongress are initialized correctly.
    """
    assert isinstance(client.amendment, Amendment)
    assert isinstance(client.bill, Bill)
    assert isinstance(client.committee, Committee)
    assert isinstance(client.communication, Communication)
    assert isinstance(client.congress, Congress)
    assert isinstance(client.member, Member)
    assert isinstance(client.nomination, Nomination)
    assert isinstance(client.record, Record)
    assert isinstance(client.summary, Summary)
    assert isinstance(client.treaty, Treaty)
