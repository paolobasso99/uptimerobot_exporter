import requests
import math
from typing import Tuple


class UptimerobotReadApi():
    """Uptimerobot API wrapper class.
    This class is used to access Uptimerobot read-only API.

    Attributes:
        BASE_URL (str): The API base URL.
    """

    BASE_URL = "https://api.uptimerobot.com/v2/"

    def __init__(self, api_key: str) -> None:
        """Create an instance

        Args:
            api_key (str): The Uptimerobot's API key
        """

        self.api_key = api_key

    def request(self, url: str, data: dict) -> Tuple[bool, dict]:
        """Make a request against the API

        Args:
            url (str): The Uptimerobot's API URL
            data (dict): The payload

        Returns:
            A Tuple where the first element is a bool that rappresent whether
            the request was successful or not.
            The second element contains the response data.

        Raises:
            RequestException: If something went wrong with the request.
        """
        response = requests.post(url, data=data)
        content = response.json()

        if content.get('stat'):
            stat = content.get('stat')
            if stat == "ok":
                return True, content
        return False, content

    def get_monitors_paginated(self, optional_params: dict = {}) -> Tuple[bool, dict]:
        """
        Returns the API response for one page of known monitors.
        https://uptimerobot.com/api/#getMonitorsWrap

        Args:
            optional_params (dict): Optional parameters to include in the API call. Do not include the api_key.
                See https://uptimerobot.com/api/#getMonitorsWrap.
                example: optional_params = {
                    "offset": "100"
                    "response_times": "1"
                }

        Returns:
            A Tuple where the first element is a bool that rappresent whether
            the request was successful or not.
            The second element contains the response data.

        Raises:
            RequestException: If something went wrong with the request.
            AttributeError: If optional_params is not a dict.
        """

        # Check optional_params attribute
        if optional_params is not None and (not isinstance(optional_params, dict)):
            raise AttributeError("optional_params has to be a dictionary")

        url = f'{self.BASE_URL}getMonitors?format=json'
        data = {
            'api_key': self.api_key
        }

        if len(optional_params) > 0:
            data.update(optional_params)

        return self.request(url, data)

    def get_monitors(self, optional_params: dict = None) -> Tuple[bool, list]:
        """
        Returns the API response for all known monitors.
        https://uptimerobot.com/api/#getMonitorsWrap

        Args:
            optional_params (dict): Optional parameters to include in the API call. Do not include the api_key or an offset.
                See https://uptimerobot.com/api/#getMonitorsWrap.
                example: optional_params = {
                    "response_times": "1"
                    "response_times_limit": "4"
                }

        Returns:
            A Tuple where the first element is a bool that rappresent whether
            the requests were successful or not.
            The second element contains the monitors data.

        Raises:
            RequestException: If something went wrong with the request.
            AttributeError: If optional_params is not a dict.
        """
        
        # Check optional_params attribute
        if optional_params is not None and (not isinstance(optional_params, dict)):
            raise AttributeError("optional_params has to be a dictionary")

        # Initialize optional_params
        if optional_params is None:
            optional_params = {}

        monitors = []

        success = True
        condition = True
        offset = 0
        while condition:
            optional_params["offset"] = offset
            
            status, page = self.get_monitors_paginated(optional_params)

            if status:
                monitors += page["monitors"]
                offset += page["pagination"]["limit"]
                condition = page["pagination"]["total"] >= (
                    page["pagination"]["limit"] + page["pagination"]["offset"])
            else:
                success = False
                condition = False

        return success, monitors
