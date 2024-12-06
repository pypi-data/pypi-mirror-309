from .base import BaseCongress
from .amendment import Amendment
from .bill import Bill
from .committee import Committee
from .communication import Communication
from .congress import Congress
from .member import Member
from .nomination import Nomination
from .record import Record
from .summary import Summary
from .treaty import Treaty

class PyCongress(BaseCongress):
    """
    Main class for interacting with the Congress.gov API.
    """
    def __init__(self, apikey: str):
        super().__init__(apikey, "https://api.congress.gov/v3/")

        self.amendment = Amendment(self)
        self.bill = Bill(self)
        self.committee = Committee(self)
        self.communication = Communication(self)
        self.congress = Congress(self)
        self.member = Member(self)
        self.nomination = Nomination(self)
        self.record = Record(self)
        self.summary = Summary(self)
        self.treaty = Treaty(self)
