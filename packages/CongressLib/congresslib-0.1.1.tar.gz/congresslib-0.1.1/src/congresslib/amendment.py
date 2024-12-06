from .base import BaseCongress
from .setting import (DEFAULT_LIMIT, AMENDMENT_LIST)
from .utils import *
from typing import Dict, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .main import PyCongress

class Amendment(BaseCongress):
    """
    Handles functionality related to amendments in the Congress.gov API
    """
    def __init__(self, client: "PyCongress"):
        """
        Initialize the Amendment class with a reference to the PyCongress client.

        Args:
            client (PyCongress): The PyCongress client instance.
        """
        super().__init__(client.apikey, client.base_url)

    def get_amendment_list(
        self,
        congress: Optional[int] = None,
        type: Optional[int] = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of amendments.
        
        Args:
            congress (Optional[int]): The congress number.
            type (Optional[str]): The type of amendment. Value can be "h", "s", "su".
            offset (int): The starting records returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).
            from_date (str): The start time.
            to_date (str): the end time.

        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raises:
            ValueError: If "type" has an invalid value.
            ValueError: If "type" is specified and "congress" is not.
        """
        if type is not None and congress is None:
            raise ValueError("'congres' must be specified when 'type' is provided.")
        if type is not None and type not in AMENDMENT_LIST:
            raise ValueError("Invalid amendment type.")
        
        endpoint = "amendment"
        if congress is not None:
            endpoint = f"{endpoint}/{congress}"
        if type is not None:
            endpoint = f"{endpoint}/{type}amdt"
        
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }
        if from_date is not None:
            params["fromDateTime"] = format_date(from_date)
        if to_date is not None:
            params["toDateTiem"] = format_date(to_date)
        
        return self._get(endpoint=endpoint, params=params)["amendments"]
    
    def get_amendment(
        self,
        congress: int,
        type: str,
        number: int,
    ) -> Optional[Dict]:
        """
        Retrieve detailed information about a specified amendment.
        
        Args:
            congress (int): The congress number.
            type (str): The type of amendment. Value can be "h", "s", "su".
            number (int): The amendment's assigned number.
        
        Returns:
            Optional[Dict]: The JSON response from the API.

        Raises:
            ValueError: If "type" has an invalid value.
        """
        if type is not None and type not in AMENDMENT_LIST:
            raise ValueError("Invalid amendment type.")
        endpoint = f"amendment/{congress}/{type}/{number}"
        params = {"api_key": self.apikey, "format": "json"}

        return self._get(endpoint=endpoint, params=params)["amendment"]
    
    def get_amendment_actions(
        self,
        congress: int,
        type: str,
        number: int,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve the list of actions on a specified amendment.
        
        Args:
            congress (int): The congress number.
            type (str): The type of amendment. Value can be "h", "s", "su".
            number (int): The amendment's assigned number.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).        
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raises:
            ValueError: If "type" has an invalid value.
        """
        if type is not None and type not in AMENDMENT_LIST:
            raise ValueError("Invalid amendment type.")
        endpoint = f"amendment/{congress}/{type}amdt/{number}/actions"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["actions"]
    
    def get_amendment_cosponsors(
        self,
        congress: int,
        type: str,
        number: int,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve the list of cosponsors on a specified amendment.
        
        Args:
            congress (int): The congress number.
            type (str): The type of amendment. Value can be "h", "s", "su".
            number (int): The amendment's assigned number.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).        
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raises:
            ValueError: If "type" has an invalid value.
        """
        if type is not None and type not in AMENDMENT_LIST:
            raise ValueError("Invalid amendment type.")
        endpoint = f"amendment/{congress}/{type}amdt/{number}/cosponsors"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["cosponsors"]
    
    def get_amendment_amendments(
        self,
        congress: int,
        type: str,
        number: int,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve the list of amendments to a specified amendment.
        
        Args:
            congress (int): The congress number.
            type (str): The type of amendment. Value can be "h", "s", "su".
            number (int): The amendment's assigned number.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raises:
            ValueError: If "type" has an invalid value.
        """
        if type is not None and type not in AMENDMENT_LIST:
            raise ValueError("Invalid amendment type.")
        endpoint = f"amendment/{congress}/{type}amdt/{number}/amendments"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["amendments"]
    
    def get_amendment_text(
        self,
        congress: int,
        type: str,
        number: int,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve the list of text versions for a specified amendment from the 117th Congress onwards.
        
        Args:
            congress (int): The congress number.
            type (str): The type of amendment. Value can be "h", "s", "su".
            number (int): The amendment's assigned number.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).        
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raises:
            ValueError: If "type" has an invalid value.
            ValueError: If "congress" is out of bound.
        """
        if type is not None and type not in AMENDMENT_LIST:
            raise ValueError("Invalid amendment type.")
        if congress < 117:
            raise ValueError("The endpoint is only available for the 117th Congress onwards.")
        
        endpoint = f"amendment/{congress}/{type}amdt/{number}/text"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["textVersions"]