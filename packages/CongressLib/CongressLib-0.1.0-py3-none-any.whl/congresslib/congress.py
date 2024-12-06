from .base import BaseCongress
from .setting import (DEFAULT_LIMIT)
from .utils import *
from typing import Dict, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .main import PyCongress

class Congress(BaseCongress):
    """   
    Handles functionality related to congress in the Congress.gov API
    """
    def __init__(self, client: "PyCongress"):
        """
        Initialize the Amendment class with a reference to the PyCongress client.

        Args:
            client (PyCongress): The PyCongress client instance.
        """
        super().__init__(client.apikey, client.base_url)

    def get_congress_list(
        self,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of congresses and congressional sessions.
        
        Args:
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).

        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        """
        endpoint = "congress"
        params = {
            "api_key": self,
            "format": "json",
            "offset": offset,
            "limit": limit
        }
        return self._get(endpoint=endpoint, params=params)["congresses"]
    
    def get_congress(self, congress: int) -> Optional[Dict]:
        """
        Retrieve detailed information for a specified congress.
        
        Args:
            congress (int): The congress number.

        Returns:
            Optional[Dict]: The JSON response from the API.
        """
        endpoint = f"congress/{congress}"
        params = {"api_key": self.apikey, "format": "json"}
        return self._get(endpoint=endpoint, params=params)["congress"]
    
    def get_current_congress(self) -> Optional[Dict]:
        """
        Retrieve detailed information for the current congress.
        
        Returns:
            Optional[Dict]: The JSON response from the API.
        """
        endpoint = f"congress/current"
        params = {"api_key": self.apikey, "format": "json"}
        return self._get(endpoint=endpoint, params=params)["congress"]