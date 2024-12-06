from py_congress.base import BaseCongress
from .setting import (DEFAULT_LIMIT)
from .utils import *
from typing import Dict, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .main import PyCongress

class Record(BaseCongress):
    """   
    Handles functionality related to records in the Congress.gov API
    """
    def __init__(self, client: "PyCongress"):
        """
        Initialize the Amendment class with a reference to the PyCongress client.

        Args:
            client (PyCongress): The PyCongress client instance.
        """
        super().__init__(client.apikey, client.base_url)

    def get_record_list(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of congressional record issues.

        Args:
            year (Optional[int]): The year the issue was published.
            month (Optional[int]): The month the issue was published.
            day (Optional[int]): The day the issue was published.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.

        Raise:
            ValueError: If "day" is specified and "month" or "year" is not.
            ValueError: If "month" is specified and "year" is not.
        """
        if day is not None and month is None:
            raise ValueError("Month must be specified when day is provided.")
        if month is not None and year is None:
            raise ValueError("Year must be specified when month is provided.")
        
        endpoint = "congressional-record"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }
        if year is not None:
            params["y"] = year
        if month is not None:
            params["m"] = month
        if day is not None:
            params["d"] = day
        
        return self._get(endpoint=endpoint, params=params)["Results"]
    
    def get_daily_record_list(
        self,
        volume: Optional[str] = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of daily congressional record issues.

        Args:
            volume (Optional[str]): The specified volume of the daily Congressional record.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        """
        endpoint = "daily-congressional-record"
        if volume is not None:
            endpoint = f"{endpoint}/{volume}"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["dailyCongressionalRecord"]
    
    def get_daily_record(
        self,
        volume: str = None,
        issue: str = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[Dict]:
        """
        Retrieve the daily congressional record filtered by volume and issue.
        
        Args:
            volume (str): The specified volume of the daily Congressional record.
            issue (str): The specified issue of the daily Congressional record.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).
        
        Returns:
            Optional[Dict]: The JSON response from the API.
        """
        endpoint = f"daily-congressional-record/{volume}/{issue}"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["issue"][0]
    
    def get_daily_record_articles(
        self,
        volume: str = None,
        issue: str = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve the list of daily congressional record articles filtered by volume and issue.
        
        Args:
            volume (str): The specified volume of the daily Congressional record.
            issue (str): The specified issue of the daily Congressional record.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).
        
        Returns:
            Optional[List[Dict]]: The JSON response from the API.
        """
        endpoint = f"daily-congressional-record/{volume}/{issue}/articles"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }

        return self._get(endpoint=endpoint, params=params)["articles"]
    
    def get_bound_record_list(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT
    ) -> Optional[List[Dict]]:
        """
        Retrieve a list of bound congressional records.

        Args:
            year (Optional[int]): The year of the bound Congressional record.
            month (Optional[int]): The month of the bound Congressional record.
            day (Optional[int]): The day of the bound Congressional record.
            offset (int): The starting record returned (default: 0).
            limit (int): The number of records returned (default: 250) (max: 250).
        
        Returns:
            Optional[Dict]: The JSON response from the API.

        Raise:
            ValueError: If "day" is specified and "month" or "year" is not.
            ValueError: If "month" is specified and "year" is not.
        """
        if day is not None and month is None:
            raise ValueError("Month must be specified when day is provided.")
        if month is not None and year is None:
            raise ValueError("Year must be specified when month is provided.")
        endpoint = "bound-congressional-record"
        params = {
            "api_key": self.apikey,
            "format": "json",
            "offset": offset,
            "limit": limit
        }
        if year is not None:
            params["year"] = year
        if month is not None:
            params["month"] = month
        if day is not None:
            params["day"] = day
        
        return self._get(endpoint=endpoint, params=params)["boundCongressionalRecord"]