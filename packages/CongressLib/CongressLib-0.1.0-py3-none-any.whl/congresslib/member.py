from py_congress.base import BaseCongress
from .setting import (DEFAULT_LIMIT)
from .utils import *
from typing import Dict, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .main import PyCongress

class Member(BaseCongress):
    """
    Handles functionality related to members in the Congress.gov API
    """
    def __init__(self, client: "PyCongress"):
        """
        Initialize the Amendment class with a reference to the PyCongress client.

        Args:
            client (PyCongress): The PyCongress client instance.
        """
        super().__init__(client.apikey, client.base_url)

    def get_member_list(
        self,
        congress: Optional[int] = None,
        state: Optional[str] = None,
        district: Optional[int] = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        current_member: bool = False
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of members.

        Args:
            congress (Optional[int]): The congress number.
            state (Optional[str]): The two letter identifier for the state the member represents.
            district (Optional[int]): The district number for the district the member represents.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).
            from_date (Optional[str]): The starting time.
            to_date (Optional[str]): The end time.
            current_member (bool): Whether the member is a current member (default: False).

        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raises:
            ValueError: If "district" is specified and "state" is not
        """
        if district is not None and state is None:
            raise ValueError("'state' must be specified when 'district' is provided.")
        endpoint = "member"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "currentMember": current_member
        }
        if congress is not None:
            endpoint = f"{endpoint}/congress/{congress}"
            if state is not None:
                endpoint = f"{endpoint}/{state}"
                if district is not None:
                    endpoint = f"{endpoint}/{district}"
                return self._get(endpoint=endpoint, params=params)["members"]
            else:
                params["offset"] = offset
                params["limit"] = limit
                return self._get(endpoint=endpoint, params=params)["members"]
        elif state is not None:
            endpoint = f"{endpoint}/{state}"
            if district is not None:
                endpoint = f"{endpoint}/{district}"
            return self._get(endpoint=endpoint, params=params)["members"]
        else:
            params["offset"] = offset
            params["limit"] = limit
            if from_date is not None:
                params["fromDateTime"] = format_date(from_date)
            if to_date is not None:
                params["toDateTime"] = format_date(to_date)
            return self._get(endpoint=endpoint, params=params)["members"]
    
    def get_member(self, id: str) -> Optional[Dict]:
        """
        Retrieve detailed biographical information about a specified mmeber.
        
        Args:
            id (str): The bioguide identifier for the congressional member.
        
        Returns:
            Optional[Dict]: The JSON response from the API.
        """
        endpoint = f"member/{id}"
        params = {"api_key": self.apikey, "format": "json"}
        return self._get(endpoint=endpoint, params=params)["member"]

    def get_sponsored_legislation(
        self,
        id: str,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve the list of legislation sponsored by a specified congressional member.
        
        Args:
            id (str): The bioguide identifier for the congressional member.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).

        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        """
        endpoint = f"member/{id}/sponsored-legislation"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }
        return self._get(endpoint=endpoint, params=params)["sponsoredLegislation"]

    def get_cosponsored_legislation(
        self,
        id: str,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve the list of legislation cosponsored by a specified congressional member.
        
        Args:
            id (str): The bioguide identifier for the congressional member.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).

        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        """
        endpoint = f"member/{id}/cosponsored-legislation"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }
        return self._get(endpoint=endpoint, params=params)["cosponsoredLegislation"]

