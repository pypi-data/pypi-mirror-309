import requests

class BaseCongress:
    """
    Base class for all Congress.gov API-related classes.
    """
    def __init__(self, apikey: str, base_url: str):
        """
        Initialize the base class with shared attributes.

        Args:
            apikey (str): The API key for Congress.gov.
            base_url (str): The base URL for the API.
        """
        self.apikey = apikey
        self.base_url = base_url

    def _get(self, endpoint: str, params: dict = None) -> dict:
        """
        Make a GET request to the Congress API.

        Args:
            endpoint (str): The API endpoint.
            params (dict): Query parameters for the request.

        Returns:
            dict: The JSON response from the API.
        """
        if params is None:
            params = {}
        params["api_key"] = self.apikey
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
