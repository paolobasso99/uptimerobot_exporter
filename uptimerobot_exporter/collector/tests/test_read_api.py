import unittest
from unittest.mock import Mock, patch
from ..read_api import UptimerobotReadApi, requests


class TestReadApi(unittest.TestCase):
    """Test for UptimerobotReadApi"""

    def test_request(self):
        """Test that the request method works correctly"""

        response_mock = Mock()
        read_api = UptimerobotReadApi("api-key")

        # 1. Correct request
        response_mock.json.return_value = {
            "stat": "ok"
        }
        requests.post = Mock(return_value=response_mock)

        self.assertEqual(
            read_api.request("path", data={}),
            (True, response_mock.json.return_value),
            "Should correctly return from the api"
        )
        requests.post.assert_called_once_with(
            read_api.BASE_URL + "path", data={})

        # 2. Something wrong with the API
        response_mock.json.return_value = {
            "stat": "fail"
        }
        requests.post = Mock(return_value=response_mock)

        self.assertEqual(
            read_api.request("path", data={}),
            (False, response_mock.json.return_value),
            "The first element of the Tuple should be false"
        )

    def test_get_monitors_paginated(self):
        """Test that the get_monitors_paginated method works correctly"""

        read_api = UptimerobotReadApi("api-key")

        read_api.request = Mock(return_value=(True, {}))

        # 1. No optional params
        read_api.get_monitors_paginated()
        read_api.request.assert_called_once_with("getMonitors", {
            'api_key': "api-key",
            'format': 'json'
        })

        # 2. Has to include optional params
        read_api.request.reset_mock()
        read_api.get_monitors_paginated({
            "optional-param": "value"
        })
        read_api.request.assert_called_once_with("getMonitors", {
            'api_key': "api-key",
            'format': 'json',
            "optional-param": "value"
        })

    def mock_request_for_test_get_monitors(self, data):
        """Mock for UptimerobotReadApi.request to test get_monitors"""
        return (True, {
            "stat": "ok",
            "pagination": {
                "offset": data["offset"],
                "limit": 2,
                "total": 6
            },
            "monitors": [
                {
                    "monitor" + str(data["offset"]+1): "monitor_name"
                },
                {
                    "monitor" + str(data["offset"]+2): "monitor_name"
                }
            ]
        })

    @patch.object(UptimerobotReadApi, 'request', side_effect=mock_request_for_test_get_monitors)
    def test_get_monitors(self, mock_method):
        """Test that the get_monitors method works correctly"""

        read_api = UptimerobotReadApi("api-key")

        status, monitors = read_api.get_monitors()

        assert status is True
        assert len(monitors) == 6


if __name__ == '__main__':
    unittest.main()
