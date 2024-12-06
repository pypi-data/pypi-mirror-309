from py_congress.base import BaseCongress
from .setting import (DEFAULT_LIMIT)
from .utils import *
from typing import Dict, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .main import PyCongress

class Treaty(BaseCongress):
    """
    Handles functionality related to treaties in the Congress.gov API
    """
    def __init__(self, client: "PyCongress"):
        """
        Initialize the Amendment class with a reference to the PyCongress client.

        Args:
            client (PyCongress): The PyCongress client instance.
        """
        super().__init__(client.apikey, client.base_url)

    def get_treaty_list(
        self,
        congress: Optional[int] = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of treaties.

        Args:
            congress (Optional[int]): The congress number.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).
            from_date (Optional[str]): The start date.
            to_date(Optional[str]): The end date.

        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        """
        endpoint = "treaty"
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

        return self._get(endpoint=endpoint, params=params)["treaties"]
    
    def get_treaty(
        self,
        congress: int,
        number: int,
        suffix: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Retrieve detailed information for a specified or specified partitioned treaty.

        Args:
            congress (int): The congress number.
            number (int): The treaty's assigned number.
            suffix (Optional[str]): The treaty's partition letter value.

        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        """
        endpoint = f"treaty/{congress}/{number}"
        if suffix is not None:
            endpoint = f"{endpoint}/{suffix}"
        params = {"api_key": self.apikey, "format": "json"}

        return self._get(endpoint=endpoint, params=params)["treaty"]
    
    def get_treaty_actions(
        self,
        congress: int,
        number: int,
        suffix: Optional[str] = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[Dict]:
        """
        Retrieve a list of actions on a specified treaty or specified partitioned treaty.

        Args:
            congress (int): The congress number.
            number (int): The treaty's assigned number.
            suffix (Optional[str]): The treaty's partition letter value.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).

        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        """
        if suffix is None:
            endpoint = f"treaty/{congress}/{number}/actions"
        else:
            endpoint = f"treaty/{congress}/{number}/{suffix}/actions"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["actions"]
    
    def get_treaty_committees(
        self,
        congress: int,
        number: int,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[Dict]:
        """
        Retrieve a list of committees associated with a specified treaty.

        Args:
            congress (int): The congress number.
            number (int): The treaty's assigned number.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).

        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        """
        endpoint = f"treaty/{congress}/{number}/committees"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["treatyCommittees"]

