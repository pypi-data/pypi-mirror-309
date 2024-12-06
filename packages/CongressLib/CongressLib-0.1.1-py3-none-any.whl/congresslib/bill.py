from .base import BaseCongress
from .setting import (DEFAULT_LIMIT, BILL_LIST, LAW_LIST, SORT_LIST)
from .utils import *
from typing import Dict, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .main import PyCongress

class Bill(BaseCongress):
    """
    Handles functionality related to bills in the Congress.gov API
    """
    def __init__(self, client: "PyCongress"):
        """
        Initialize the Amendment class with a reference to the PyCongress client.

        Args:
            client (PyCongress): The PyCongress client instance.
        """
        super().__init__(client.apikey, client.base_url)

    def get_bill_list(
        self,
        congress: Optional[int] = None,
        type: Optional[str] = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        sort: str = "desc"
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of bills.
        
        Args:
            congress (Optional[int]): The congress number. Must be specified if type is specified.
            type (Optional[str]): The type of bill. Value can be "hr", "s", "hjres", "sjres", "hconres", "sconres", "hres", or "sres".
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).
            from_date (Optional[str]): The start date.
            to_date(Optional[str]): The end date.
            sort (str): Sort order, either "asc" or "desc" (default: "desc").
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        
        Raises:
            ValueError: If "sort" has an invalid value.
            ValueError: If "type" has an invalid value.
            ValueError: If "type" is specified and "congress" is not
        """
        endpoint = "bill"

        if type is not None and congress is None:
            raise ValueError("'congres' must be specified when 'type' is provided.")

        if type is not None and type not in BILL_LIST:
            raise ValueError("Invalid bill type.")

        if sort not in SORT_LIST:
            raise ValueError("Invalid sort order. Must be either 'asc' or 'dsec'.")
        
        if congress is not None:
            endpoint = f"{endpoint}/{congress}"
        if type is not None:
            endpoint =f"{endpoint}/{type}"

        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit,
            "sort": f"updateDate+{sort}"
        }
        if from_date is not None:
            params["fromDateTime"] = format_date(from_date)
        if to_date is not None:
            params["toDateTime"] = format_date(to_date)

        return self._get(endpoint=endpoint, params=params)["bills"]
    
    def get_bill(
        self,
        congress: int,
        type: str,
        number: int,
    ) -> Optional[Dict]:
        """
        Retrieve detailed information about a specified bill.
        
        Args:
            congress (int): The congress number.
            type (str): The type of bill. Value can be "hr", "s", "hjres", "sjres", "hconres", "sconres", "hres", or "sres".
            number (int): The bill's assigned number.
        
        Returns:
            Optional[Dict]: The JSON response from the API.

        Raises:
            ValueError: If "type" has an invalid value.
        """
        if type is not None and type not in BILL_LIST:
            raise ValueError("Invalid bill type.")
        endpoint = f"bill/{congress}/{type}/{number}"
        params = {"api_key": self.apikey, "format": "json"}

        return self._get(endpoint=endpoint, params=params)["bill"]
    
    def get_bill_actions(
        self,
        congress: int,
        type: str,
        number: int,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve the list of actions on a specified bill.
        
        Args:
            congress (int): The congress number.
            type (str): The type of bill. Value can be "hr", "s", "hjres", "sjres", "hconres", "sconres", "hres", or "sres".
            number (int): The bill's assigned number.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).        
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raises:
            ValueError: If "type" has an invalid value.
        """
        if type is not None and type not in BILL_LIST:
            raise ValueError("Invalid bill type.")
        endpoint = f"bill/{congress}/{type}/{number}/actions"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["actions"]
    
    def get_bill_amendments(
        self,
        congress: int,
        type: str,
        number: int,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve the list of amendments on a specified bill.
        
        Args:
            congress (int): The congress number.
            type (str): The type of bill. Value can be "hr", "s", "hjres", "sjres", "hconres", "sconres", "hres", or "sres".
            number (int): The bill's assigned number.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).        
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raises:
            ValueError: If "type" has an invalid value.
        """
        if type is not None and type not in BILL_LIST:
            raise ValueError("Invalid bill type.")
        endpoint = f"bill/{congress}/{type}/{number}/amendments"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["amendments"]
    
    def get_bill_committees(
        self,
        congress: int,
        type: str,
        number: int,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve the list of committees associated with a specified bill.
        
        Args:
            congress (int): The congress number.
            type (str): The type of bill. Value can be "hr", "s", "hjres", "sjres", "hconres", "sconres", "hres", or "sres".
            number (int): The bill's assigned number.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).        
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raises:
            ValueError: If "type" has an invalid value.
        """
        if type is not None and type not in BILL_LIST:
            raise ValueError("Invalid bill type.")
        endpoint = f"bill/{congress}/{type}/{number}/committees"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["committees"]
    
    def get_bill_cosponsors(
        self,
        congress: int,
        type: str,
        number: int,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve the list of cosponsors on a specified bill.
        
        Args:
            congress (int): The congress number.
            type (str): The type of bill. Value can be "hr", "s", "hjres", "sjres", "hconres", "sconres", "hres", or "sres".
            number (int): The bill's assigned number.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).        
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raises:
            ValueError: If "type" has an invalid value.
        """
        if type is not None and type not in BILL_LIST:
            raise ValueError("Invalid bill type.")
        endpoint = f"bill/{congress}/{type}/{number}/cosponsors"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["cosponsors"]
    
    def get_bill_relatedbills(
        self,
        congress: int,
        type: str,
        number: int,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve the list of related bills to a specified bill.
        
        Args:
            congress (int): The congress number.
            type (str): The type of bill. Value can be "hr", "s", "hjres", "sjres", "hconres", "sconres", "hres", or "sres".
            number (int): The bill's assigned number.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).        
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raises:
            ValueError: If "type" has an invalid value.
        """
        if type is not None and type not in BILL_LIST:
            raise ValueError("Invalid bill type.")
        endpoint = f"bill/{congress}/{type}/{number}/relatedbills"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["relatedBills"]
    
    def get_bill_subjects(
        self,
        congress: int,
        type: str,
        number: int,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve the list of legislative subjects on a specified bill.
        
        Args:
            congress (int): The congress number.
            type (str): The type of bill. Value can be "hr", "s", "hjres", "sjres", "hconres", "sconres", "hres", or "sres".
            number (int): The bill's assigned number.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).        
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raises:
            ValueError: If "type" has an invalid value.
        """
        if type is not None and type not in BILL_LIST:
            raise ValueError("Invalid bill type.")
        endpoint = f"bill/{congress}/{type}/{number}/subjects"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["subjects"]
    
    def get_bill_summaries(
        self,
        congress: int,
        type: str,
        number: int,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve the list of summaries for a specified bill.
        
        Args:
            congress (int): The congress number.
            type (str): The type of bill. Value can be "hr", "s", "hjres", "sjres", "hconres", "sconres", "hres", or "sres".
            number (int): The bill's assigned number.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).        
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raises:
            ValueError: If "type" has an invalid value.
        """
        if type is not None and type not in BILL_LIST:
            raise ValueError("Invalid bill type.")
        endpoint = f"bill/{congress}/{type}/{number}/summaries"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["summaries"]
    
    def get_bill_text(
        self,
        congress: int,
        type: str,
        number: int,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve the list of text versions for a specified fill.
        
        Args:
            congress (int): The congress number.
            type (str): The type of bill. Value can be "hr", "s", "hjres", "sjres", "hconres", "sconres", "hres", or "sres".
            number (int): The bill's assigned number.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).        
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raises:
            ValueError: If "type" has an invalid value.
        """
        if type is not None and type not in BILL_LIST:
            raise ValueError("Invalid bill type.")
        endpoint = f"bill/{congress}/{type}/{number}/text"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["textVersions"]
    
    def get_bill_titles(
        self,
        congress: int,
        type: str,
        number: int,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve the list of titles for a specified bill.
        
        Args:
            congress (int): The congress number.
            type (str): The type of bill. Value can be "hr", "s", "hjres", "sjres", "hconres", "sconres", "hres", or "sres".
            number (int): The bill's assigned number.
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).        
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raises:
            ValueError: If "type" has an invalid value.
        """
        if type is not None and type not in BILL_LIST:
            raise ValueError("Invalid bill type.")
        endpoint = f"bill/{congress}/{type}/{number}/titles"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["titles"]
    
    def get_law_list(
        self,
        congress: int,
        type: Optional[str] = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of laws.
        
        Args:
            congress (int): The congress number.
            type (Optional[str]): The law type. Values are either "pub" or "priv".
            offset (int): The starting record returned. (default: 0).
            limit (int): The number of records to retrieve (default: 250, max: 250).
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raises:
            ValueError: If "type" has an invalid value.
        """
        if type is not None and type not in LAW_LIST:
            raise ValueError("Invalid law type.")
        endpoint = f"law/{congress}"
        if type is not None:
            endpoint = f"{endpoint}/{type}"

        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["bills"]
    
    def get_law(
        self,
        congress: int,
        type: str,
        number: int,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[Dict]:
        """
        Retrieve a law filtered by specified congress, law type, and number.
        
        Args:
            congress (int): The congress number.
            type (str): The law type. Values are either "pub" or "priv".
            number (int): The law number.
        
        Returns:
            Optional[Dict]: The JSON response from the API.

        Raises:
            ValueError: If "type" has an invalid value.
        """
        if type is not None and type not in LAW_LIST:
            raise ValueError("Invalid law type.")
        endpoint = f"law/{congress}/{type}/{number}"
        params = {
            "api_key":self.apikey,
            "format":"json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["bill"]