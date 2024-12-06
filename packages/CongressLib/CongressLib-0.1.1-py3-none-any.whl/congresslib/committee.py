from .base import BaseCongress
from .setting import (DEFAULT_LIMIT, CHAMBER_LIST, PRINT_LIST, REPORT_LIST)
from .utils import *
from typing import Dict, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .main import PyCongress

class Committee(BaseCongress):
    """   
    Handles functionality related to committees in the Congress.gov API
    """
    def __init__(self, client: "PyCongress"):
        """
        Initialize the Amendment class with a reference to the PyCongress client.

        Args:
            client (PyCongress): The PyCongress client instance.
        """
        super().__init__(client.apikey, client.base_url)

    def get_committee_list(
        self,
        congress: Optional[int] = None,
        chamber: Optional[str] = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of congressional committees.
        
        Args:
            congress (Optional[int]): The congress number.
            chamber (Optional[str]): The chamber name. Value can be "house", "senate", or "joint".
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).
            from_date (Optional[str]): The start time.
            to_date (Optional[str]): The end time.

        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raise:
            ValueError: If "chamber" has an invalid value.
        """
        if chamber is not None and chamber not in CHAMBER_LIST:
            raise ValueError("Invalid chamber type.")
        endpoint = "committee"
        if congress is not None:
            endpoint = f"{endpoint}/{congress}"
        if chamber is not None:
            endpoint = f"{endpoint}/{chamber}"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }
        if from_date is not None:
            params["fromDateTime"] = format_date(from_date)
        if to_date is not None:
            params["toDateTime"] = format_date(to_date)
        
        return self._get(endpoint=endpoint, params=params)["committees"]
    
    def get_committee(self, chamber: str, code: str) -> Optional[Dict]:
        """
        Retrieve detailed information for a specified congressional committee
        
        Args:
            chamber (str): The chamber name. Value can be "house", "senate", or "joint".
            code (str): The committee code for the committee.

        Returns:
            Optional[Dict]: The JSON response from the API.

        Raise:
            ValueError: If "chamber" has an invalid value.
        """
        if chamber not in CHAMBER_LIST:
            raise ValueError("Invalid chamber type.")
        endpoint = f"committee/{chamber}/{code}"
        params = {"api_key": self.apikey, "format": "json"}

        return self._get(endpoint=endpoint, params=params)["committee"]
    
    def get_committee_bills(
        self,
        chamber: str,
        code: str,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of legislation associated with the specified congressional committee.
        
        Args:
            chamber (str): The chamber name. Value can be "house, "senate", or "joint".
            code (str): The committee code for the committee.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).
            from_date (Optional[str]): The start time.
            to_date (Optional[str]): The end time.

        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raise:
            ValueError: If "chamber" has an invalid value.
        """
        if chamber not in CHAMBER_LIST:
            raise ValueError("Invalid chamber type.")
        endpoint = f"committee/{chamber}/{code}/bills"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }
        if from_date is not None:
            params["fromDateTime"] = format_date(from_date)
        if to_date is not None:
            params["toDateTime"] = format_date(to_date)
        
        return self._get(endpoint=endpoint, params=params)["committee-bills"]["bills"]
    
    def get_committee_reports(
        self,
        chamber: str,
        code: str,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of committee reports associated with the specified congressional committee.
        
        Args:
            chamber (str): The chamber name. Value can be "house, "senate", or "joint".
            code (str): The committee code for the committee.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).
            from_date (Optional[str]): The start time.
            to_date (Optional[str]): The end time.

        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raise:
            ValueError: If "chamber" has an invalid value.
        """
        if chamber not in CHAMBER_LIST:
            raise ValueError("Invalid chamber type.")
        endpoint = f"committee/{chamber}/{code}/reports"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }
        if from_date is not None:
            params["fromDateTime"] = format_date(from_date)
        if to_date is not None:
            params["toDateTime"] = format_date(to_date)
        
        return self._get(endpoint=endpoint, params=params)["reports"]
    
    def get_committee_nominations(
        self,
        chamber: str,
        code: str,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of nominations associated with the specified congressional committee.
        
        Args:
            chamber (str): The chamber name. Value can be "house, "senate", or "joint".
            code (str): The committee code for the committee.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).

        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raise:
            ValueError: If "chamber" has an invalid value.
        """
        if chamber not in CHAMBER_LIST:
            raise ValueError("Invalid chamber type.")
        endpoint = f"committee/{chamber}/{code}/nominations"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }
        
        return self._get(endpoint=endpoint, params=params)["nominations"]
    
    def get_committee_communications(
        self,
        chamber: str,
        code: str,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of legislation associated with the specified congressional committee.
        
        Args:
            chamber (str): The chamber name. Value can be "house, "senate".
            code (str): The committee code for the committee.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).
            from_date (Optional[str]): The start time.
            to_date (Optional[str]): The end time.

        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raise:
            ValueError: If "chamber" has an invalid value.
        """
        if chamber not in ["house", "senate"]:
            raise ValueError("Invalid chamber type.")
        endpoint = f"committee/{chamber}/{code}/{chamber}-communication"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }
        
        return self._get(endpoint=endpoint, params=params)[f"{chamber}Communications"]
    
    def get_report_list(
        self,
        congress: Optional[int] = None,
        type: Optional[str] = None,
        conference: Optional[bool] = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of committee reports.
        
        Args:
            congress (Optional[int]): The congress number.
            type (Optional[str]): The type of committee report. Value can be "h", "s", or "e".
            conference (Optional[bool]): Flag to indicate conference reports.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).
            from_date (Optional[str]): The start time.
            to_date (Optional[str]): The end time.

        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raise:
            ValueError: If "type" has an invalid value.
            ValueError: If "type" is specified and "congress" is not
        """
        endpoint = "committee-report"
        if congress is None and type is not None:
            raise ValueError("'congress' must be specified when 'type' is provided.")
        
        if type is not None and type not in REPORT_LIST:
            raise ValueError("Invalid report type.")
        
        if congress is not None:
            endpoint = f"{endpoint}/{congress}"
        if type is not None:
            endpoint = f"{endpoint}/{type}rpt"

        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }
        if conference is not None:
            params["conference"] = conference
        if from_date is not None:
            params["fromDateTime"] = format_date(from_date)
        if to_date is not None:
            params["toDateTime"] = format_date(to_date)

        return self._get(endpoint=endpoint, params=params)["reports"]
    
    def get_report(self, congress: int, type: str, id: int) -> Optional[Dict]:
        """
        Retrieve detailed information for a specified committee report.

        Args:
            congress (int): The congress number.
            type (str): The type of committee report. Value can be "h", "s", or "e"
            id (int): The committee report's assigned number.

        Returns:
            Optional[Dict]: The JSON response from the API.

        Raise:
            ValueError: If "type" has an invalid value.
        """
        if type not in REPORT_LIST:
            raise ValueError("Invalid report type.")
        endpoint = f"committee-report/{congress}/{type}rpt/{id}"
        params = {"api_key": self.apikey, "format": "json"}

        return self._get(endpoint=endpoint, params=params)["committeeReports"][0]
    
    def get_report_text(
        self,
        congress: int,
        type: str,
        id: int,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve list of texts for a specified committee report.
        
        Args:
            congress (int): The congress number.
            type (str): The type of committee report. Value can be "h", "s", or "e"
            id (int): The committee report's assigned number.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).

        Returns:
            Optional[Dict]: The JSON response from the API.

        Raise:
            ValueError: If "type" has an invalid value.
        """
        if type not in REPORT_LIST:
            raise ValueError("Invalid report type.")
        endpoint = f"committee-report/{congress}/{type}rpt/{id}/text"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["text"]
    
    def get_print_list(
        self,
        congress: Optional[int] = None,
        chamber: Optional[str] = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of committee prints.
        
        Args:
            congress (Optional[int]): The congress number.
            chamber (Optional[str]): The chamber name. Value can be "house", "senate", or "nochamber".
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).
            from_date (Optional[str]): The start time.
            to_date (Optional[str]): The end time.

        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raise:
            ValueError: If "chamber" has an invalid value.
            ValueError: If "chamber" is specified and "congress" is not
        """
        endpoint = "committee-chamber"
        if congress is None and chamber is not None:
            raise ValueError("'congress' must be specified when 'chamber' is provided.")
        
        if chamber is not None and chamber not in PRINT_LIST:
            raise ValueError("Invalid chamber type.")
        
        if congress is not None:
            endpoint = f"{endpoint}/{congress}"
        if chamber is not None:
            endpoint = f"{endpoint}/{chamber}"

        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }
        if from_date is not None:
            params["fromDateTime"] = format_date(from_date)
        if to_date is not None:
            params["toDateTime"] = format_date(to_date)

        return self._get(endpoint=endpoint, params=params)["committeePrints"]
    
    def get_print(self, congress: int, chamber: str, jacket: int) -> Optional[Dict]:
        """
        Retrieve detailed information for a specified committee print.

        Args:
            congress (int): The congress number.
            chamber (str): The chamber name. Value can be "house", "senate", or "nochamber"
            jacket (int): The jacket number for the print.

        Returns:
            Optional[Dict]: The JSON response from the API.

        Raise:
            ValueError: If "chamber" has an invalid value.
        """
        if chamber not in PRINT_LIST:
            raise ValueError("Invalid chamber type.")
        endpoint = f"committee-print/{congress}/{chamber}/{jacket}"
        params = {"api_key": self.apikey, "format": "json"}

        return self._get(endpoint=endpoint, params=params)["committeePrint"][0]
    
    def get_print_text(
        self,
        congress: int,
        chamber: str,
        jacket: int,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve list of texts for a specified committee print.
        
        Args:
            congress (int): The congress number.
            chamber (str): The chamber name. Value can be "house", "senate", or "nochamber"
            jacket (int): The jacket number for the print.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).

        Returns:
            Optional[Dict]: The JSON response from the API.

        Raise:
            ValueError: If "chamber" has an invalid value.
        """
        if chamber not in PRINT_LIST:
            raise ValueError("Invalid chamber type.")
        endpoint = f"committee-print/{congress}/{chamber}/{jacket}/text"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["text"]
    
    def get_meeting_list(
        self,
        congress: Optional[int] = None,
        chamber: Optional[str] = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of committee meetings.
        
        Args:
            congress (Optional[int]): The congress number.
            chamber (Optional[str]): The chamber name. Value can be "house", "senate", or "nochamber".
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).

        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raise:
            ValueError: If "chamber" has an invalid value.
            ValueError: If "chamber" is specified and "congress" is not
        """
        endpoint = "committee-meeting"
        if congress is None and chamber is not None:
            raise ValueError("'congress' must be specified when 'chamber' is provided.")
        
        if chamber is not None and chamber not in PRINT_LIST:
            raise ValueError("Invalid chamber type.")
        
        if congress is not None:
            endpoint = f"{endpoint}/{congress}"
        if chamber is not None:
            endpoint = f"{endpoint}/{chamber}"

        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["committeeMeetings"]
    
    def get_meeting(self, congress: int, chamber: str, event: int) -> Optional[Dict]:
        """
        Retrieve detailed information for a specified committee meeting.

        Args:
            congress (int): The congress number.
            chamber (str): The chamber name. Value can be "house", "senate", or "nochamber"
            event (int): The event identifier.

        Returns:
            Optional[Dict]: The JSON response from the API.

        Raise:
            ValueError: If "chamber" has an invalid value.
        """
        if chamber not in PRINT_LIST:
            raise ValueError("Invalid chamber type.")
        endpoint = f"committee-meetings/{congress}/{chamber}/{event}"
        params = {"api_key": self.apikey, "format": "json"}

        return self._get(endpoint=endpoint, params=params)["committeeMeeting"]
    
    def get_hearing_list(
        self,
        congress: Optional[int] = None,
        chamber: Optional[str] = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of committee hearings.
        
        Args:
            congress (Optional[int]): The congress number.
            chamber (Optional[str]): The chamber name. Value can be "house", "senate", or "nochamber".
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).

        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raise:
            ValueError: If "chamber" has an invalid value.
            ValueError: If "chamber" is specified and "congress" is not
        """
        endpoint = "hearing"
        if congress is None and chamber is not None:
            raise ValueError("'congress' must be specified when 'chamber' is provided.")
        
        if chamber is not None and chamber not in PRINT_LIST:
            raise ValueError("Invalid chamber type.")
        
        if congress is not None:
            endpoint = f"{endpoint}/{congress}"
        if chamber is not None:
            endpoint = f"{endpoint}/{chamber}"

        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["hearings"]
    
    def get_hearing(self, congress: int, chamber: str, jacket: int) -> Optional[Dict]:
        """
        Retrieve detailed information for a specified hearing.

        Args:
            congress (int): The congress number.
            chamber (str): The chamber name. Value can be "house", "senate", or "nochamber"
            jacket (int): The jacket number for the hearing.

        Returns:
            Optional[Dict]: The JSON response from the API.

        Raise:
            ValueError: If "chamber" has an invalid value.
        """
        if chamber not in PRINT_LIST:
            raise ValueError("Invalid chamber type.")
        endpoint = f"hearing/{congress}/{chamber}/{jacket}"
        params = {"api_key": self.apikey, "format": "json"}

        return self._get(endpoint=endpoint, params=params)["hearing"]
    