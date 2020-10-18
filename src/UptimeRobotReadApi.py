import requests
import json


class UptimeRobotReadApi():
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.uptimerobot.com/v2/"

    def request(self, url, data):
        response = requests.post(url, data=data)
        content = response.json()

        if content.get('stat'):
            stat = content.get('stat')
            if stat == "ok":
                return True, content.get("monitors")
        return False, content

    def get_monitors(self, response_times=False, response_times_limit=False, logs=False, logs_limit=False, all_time_uptime_ratio=False):
        """
        Returns status and response payload for all known monitors.
        https://uptimerobot.com/api/#getMonitorsWrap
        """

        url = f'{self.base_url}getMonitors?format=json'
        data = {
            'api_key': self.api_key
        }

        # Options
        # Response times
        if response_times:
            data["response_times"] = 1
            if response_times_limit:
                data["response_times_limit"] = response_times_limit

        if logs:
            data["logs"] = 1
            if logs_limit:
                data["logs_limit"] = logs_limit

        if all_time_uptime_ratio:
            data["all_time_uptime_ratio"] = 1

        return self.request(url, data)
