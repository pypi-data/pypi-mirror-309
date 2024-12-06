from .base import BaseCongress
from .setting import (DEFAULT_LIMIT, HOUSE_COMM_LIST, SENATE_COMM_LIST)
from .utils import *
from typing import Dict, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .main import PyCongress

class Communication(BaseCongress):
    """
    Handles functionality related to communications in the Congress.gov API
    """
    def __init__(self, client: "PyCongress"):
        """
        Initialize the Amendment class with a reference to the PyCongress client.

        Args:
            client (PyCongress): The PyCongress client instance.
        """
        super().__init__(client.apikey, client.base_url)

    def get_communication_list(
        self,
        chamber: str,
        congress: Optional[int] = None,
        type: Optional[str] = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Return a list of House or Senate communications.

        Args:
            chamber (str): The chamber of Congress. Value can be "house" or "senate".
            congress (Optional[int]): The congress number. Must be specified when type is provided.
            type (Optional[str]): The type of communication. Value can be "ec", "ml", "pm", or "pt" for House and "ec", "pm", or "pom" for Senate.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).

        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        
        Raises:
            ValueError: if "chamber" has an invalid value.
            ValueError: If "type" has an invalid value.
            ValueError: If "type" is specified and "congress" is not
        """
        if chamber not in ["house", "senate"]:
            raise ValueError("Invalid chamber type.")
        if type is not None:
            if congress is None:
                raise ValueError("'congress' must be specified when 'type' is provided")
            if chamber == "house" and type not in HOUSE_COMM_LIST:
                raise ValueError("Invalid House communication type.")
            if chamber == "senate" and type not in SENATE_COMM_LIST:
                raise ValueError("Invalid Senate communiction type.")
        
        endpoint = f"{chamber}-communication"
        if congress is not None:
            endpoint = f"{endpoint}/{congress}"
        if type is not None:
            endpoint = f"{endpoint}/{type}"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)[f"{chamber}Communications"]
    
    def get_communication(
        self,
        chamber: str,
        congress: int,
        type: str,
        number: int,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[Dict]:
        """
        Return a list of House or Senate communications.

        Args:
            chamber (str): The chamber of Congress. Value can be "house" or "senate".
            congress (int): The congress number. Must be specified when type is provided.
            type (str): The type of communication. Value can be "ec", "ml", "pm", or "pt" for House and "ec", "pm", or "pom" for Senate.
            number (int): The communication's assigned number.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).

        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        
        Raises:
            ValueError: if "chamber" has an invalid value.
            ValueError: If "type" has an invalid value.
        """
        if chamber not in ["house", "senate"]:
            raise ValueError("Invalid chamber type.")
        if chamber == "house" and type not in HOUSE_COMM_LIST:
            raise ValueError("Invalid House communication type.")
        if chamber == "senate" and type not in SENATE_COMM_LIST:
            raise ValueError("Invalid Senate communiction type.")
        
        endpoint = f"{chamber}-communication/{congress}/{type}/{number}"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)[f"{chamber}Communication"]
    
    def get_requirement_list(self, offset: int = 0, limit: int = DEFAULT_LIMIT) -> Optional[List[Dict]]:
        """
        Retrieve a list of House requirements.

        Args:
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).

        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        """
        endpoint = "house-requirement"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["houseRequirements"]
    
    def get_requirement(self, number: str) -> Optional[Dict]:
        """
        Retrieve detailed information for a specified House requirement.

        Args:
            number (srt): The requirement's assigned number.

        Return:
            Optional[Dict]: The JSON response from the API.
        """
        endpoint = f"house-requirement/{number}"
        params = {"api_key": self.apikey, "format": "json"}

        return self._get(endpoint=endpoint, params=params)["houseRequirements"]

    def get_requirement_communications(
        self,
        number: str,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of matching communications to a House requirement.

        Args:
            number (srt): The requirement's assigned number.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).

        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        """
        endpoint = f"house-requirement/{number}/matching-communications"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["matchingCommunications"]