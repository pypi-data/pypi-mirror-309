from py_congress.base import BaseCongress
from .setting import (DEFAULT_LIMIT)
from .utils import *
from typing import Dict, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .main import PyCongress

class Nomination(BaseCongress):
    """
    Handles functionality related to nominations in the Congress.gov API
    """
    def __init__(self, client: "PyCongress"):
        """
        Initialize the Amendment class with a reference to the PyCongress client.

        Args:
            client (PyCongress): The PyCongress client instance.
        """
        super().__init__(client.apikey, client.base_url)

    def get_nomination_list(
        self,
        congress: Optional[int] = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        sort: str = "desc"
    ) -> Optional[List[Dict]]:
        """
        Return a list of nominations received from the President.

        Args:
            congress (Optional[int]): The congress number.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).
            from_date (Optional[str]): The start date.
            to_date(Optional[str]): The end date.
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        """
        endpoint = "nomination"
        if congress is not None:
            endpoint = f"{endpoint}/{congress}"
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

        return self._get(endpoint=endpoint, params=params)["nominations"]
    
    def get_nomination(self, congress: int, number: int) -> Optional[Dict]:
        """
        Return detailed information for a specified nomination.

        Args:
            congress (int): The congress number.
            number (int): The nomination's assigned number.
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        """
        endpoint = f"nomination/{congress}/{number}"
        params = {"api_key": self.apikey, "format": "json"}

        return self._get(endpoint=endpoint, params=params)["nomination"]
    
    def get_nominees(
        self,
        congress: int,
        number: int,
        ordinal: int,
        offset: int = 0,
        limit: int = 250
    ) -> Optional[List[Dict]]:
        """
        Return a list of nominees for a position within the nomination

        Args:
            congress (int): The congress number.
            number (int): The nomination's assigned number.
            ordinal (int): The ordinal number.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).

        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        """
        endpoint = f"nomination/{congress}/{number}/{ordinal}"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["nominees"]
    
    def get_nomination_actions(
        self,
        congress: int,
        number: int,
        offset: int = 0,
        limit: int = 250
    ) -> Optional[List[Dict]]:
        """
        Return a list of actions on a specified nomination.

        Args:
            congress (int): The congress number.
            number (int): The nomination's assigned number.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).

        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        """
        endpoint = f"nomination/{congress}/{number}/actions"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["actions"]
    
    def get_nomination_committeees(
        self,
        congress: int,
        number: int,
        offset: int = 0,
        limit: int = 250
    ) -> Optional[List[Dict]]:
        """
        Return a list of committees associated with a specified nomination.

        Args:
            congress (int): The congress number.
            number (int): The nomination's assigned number.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).

        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        """
        endpoint = f"nomination/{congress}/{number}/committees"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["committees"]
    
    def get_nomination_hearings(
        self,
        congress: int,
        number: int,
        offset: int = 0,
        limit: int = 250
    ) -> Optional[List[Dict]]:
        """
        Return a list of printed hearings associated with a specified nomination.

        Args:
            congress (int): The congress number.
            number (int): The nomination's assigned number.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).

        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        """
        endpoint = f"nomination/{congress}/{number}/hearings"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["hearings"]
    
    
