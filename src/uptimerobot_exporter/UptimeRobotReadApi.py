import requests
import math
from typing import Tuple


class UptimeRobotReadApi():
    """UptimeRobot API wrapper class.
    This class is used to access UptimeRobot read-only API.

    Attributes:
        BASE_URL (str): The API base URL.
    """

    BASE_URL = "https://api.uptimerobot.com/v2/"

    def __init__(self, api_key: str) -> None:
        """Create an instance

        Args:
            api_key (str): The UptimeRobot's API key
        """

        self.api_key = api_key

    def request(self, url: str, data: dict) -> Tuple[bool, dict]:
        """Make a request against the API

        Args:
            url (str): The UptimeRobot's API URL
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

    def get_monitors_paginated(self, offset: int=0, response_times: bool = False, response_times_limit: int = 0, logs: bool = False, logs_limit: int = 0) -> Tuple[bool, dict]:
        """
        Returns the API response for one page of known monitors.
        https://uptimerobot.com/api/#getMonitorsWrap

        Args:
            offset (int): The offset for pagination
            response_times (bool): Whether to include response times. Default is False.
            response_times_limit (int): How many response times to include. If <= 0 the option is ignored. Default is 0.
            logs (bool): Whether to include logs. Default is False.
            logs_limit (int): How many logs to include. If <= 0 the option is ignored. Default is 0.

        Returns:
            A Tuple where the first element is a bool that rappresent whether
            the request was successful or not.
            The second element contains the response data.

        Raises:
            RequestException: If something went wrong with the request.
        """

        url = f'{self.BASE_URL}getMonitors?format=json'
        data = {
            'api_key': self.api_key
        }

        # Options
        # Response times
        if response_times:
            data["response_times"] = 1
            if response_times_limit > 0:
                data["response_times_limit"] = response_times_limit

        if logs:
            data["logs"] = 1
            if logs_limit > 0:
                data["logs_limit"] = logs_limit

        return self.request(url, data)

    def get_monitors(self, response_times: bool = False, response_times_limit: int = 0, logs: bool = False, logs_limit: int = 0) -> Tuple[bool, list]:
        """
        Returns the API response for all known monitors.
        https://uptimerobot.com/api/#getMonitorsWrap

        Args:
            response_times (bool): Whether to include response times. Default is False.
            response_times_limit (int): How many response times to include. If <= 0 the option is ignored. Default is 0.
            logs (bool): Whether to include logs. Default is False.
            logs_limit (int): How many logs to include. If <= 0 the option is ignored. Default is 0.

        Returns:
            A Tuple where the first element is a bool that rappresent whether
            the requests were successful or not.
            The second element contains the monitors data.

        Raises:
            RequestException: If something went wrong with the request.
        """

        monitors = []

        success = True
        condition = True
        offset = 0
        while condition:
            status, page = self.get_monitors_paginated(offset, response_times, response_times_limit, logs, logs_limit)

            if status:
                monitors += page["monitors"]
                offset += page["pagination"]["limit"]
                condition = page["pagination"]["total"] >= (page["pagination"]["limit"] + page["pagination"]["offset"])
            else:
                success = False
                condition = False
        
        return success, monitors
        