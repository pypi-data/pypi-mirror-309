from py_congress.base import BaseCongress
from .setting import (DEFAULT_LIMIT, BILL_LIST, SORT_LIST)
from .utils import *
from typing import Dict, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .main import PyCongress

class Summary(BaseCongress):
    """   
    Handles functionality related to summaries in the Congress.gov API
    """
    def __init__(self, client: "PyCongress"):
        """
        Initialize the Amendment class with a reference to the PyCongress client.

        Args:
            client (PyCongress): The PyCongress client instance.
        """
        super().__init__(client.apikey, client.base_url)

    def get_summary_list(
        self,
        congress: Optional[int] = None,
        type: Optional[int] = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        sort: str = "desc"
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of summaries.
        
        Args:
            congress (Optional[int]): The congress number.
            type (Optional[str]): The type of bill. Value can be "hr", "s", "hjres", "sjres", "hconres", "sconres", "hres", "sres".
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).
            from_date (Optional[str]): The start time.
            to_date (Optional[str]): The end time.
            sort (str): Sort order, either "asc" or "desc" (default: "desc").
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        
        Raises:
            ValueError: If "sort" has an invalid value.
            ValueError: If "type" has an invalid value.
            ValueError: If "type" is specified and "congress" is not
        """
        endpoint = "summaries"
        if type is not None and congress is None:
            raise ValueError("'congres' must be specified when 'type' is provided.")
        if type is not None and type not in BILL_LIST:
            raise ValueError("Invalid bill type.")
        if sort not in SORT_LIST:
            raise ValueError("Invalid sort order. Must be either 'asc' or 'dsec'.")

        if congress is not None:
            endpoint = f"{endpoint}/{congress}"
        if type is not None:
            endpoint = f"{endpoint}/{type}"

        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit,
            "sort": sort
        }

        if from_date is not None:
            params["fromDateTime"] = format_date(from_date)
        if to_date is not None:
            params["toDateTime"] = format_date(to_date)
        
        return self._get(endpoint=endpoint, params=params)["summaries"]