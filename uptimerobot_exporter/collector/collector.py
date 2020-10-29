import logging
import time

from prometheus_client import Gauge
from requests import RequestException

from .read_api import UptimerobotReadApi


class UptimerobotCollector():
    """Metrics collector class.
    This class is used to access collect Uptimerobot metrics.

    Attributes:
        METRICS (dict): The metrics to collect.
        API_OPTIONAL_PARAMS (dict): The optional params used to make the API call.
    """

    # Define metrics
    METRICS = {
        'up': Gauge('uptimerobot_up',
                    'The last scrape was successful'),
        'scrape_duration_milliseconds': Gauge('uptimerobot_scrape_duration_milliseconds',
                                         'The duration of the last scrape in seconds'),
        'monitor_status': Gauge('uptimerobot_monitor_status',
                                'Status of the monitor: 0 = paused, 1 = not checked, 2 = up, 8 = seems down, 9 = down',
                                ['id', 'url', 'name', 'type']),
        'monitor_response_time': Gauge('uptimerobot_monitor_response_time_millisecond',
                                       'Last response time of the monitor in milliseconds',
                                       ['id', 'url', 'name', 'type', 'status']),
        'monitor_response_time_average': Gauge('uptimerobot_monitor_response_time_average_milliseconds',
                                               'Average response time of the monitor in milliseconds',
                                               ['id', 'url', 'name', 'type']),
        'monitor_log_type': Gauge('uptimerobot_monitor_log_type',
                                  'Last log type of the monitor: 1 = down, 2 = up, 98 = started, 99 = paused',
                                  ['id', 'url', 'name', 'type']),
        'monitor_log_datetime': Gauge('uptimerobot_monitor_log_datetime',
                                      'Last log of the monitor datetime',
                                      ['id', 'url', 'name', 'type', 'logtype'])
    }

    API_OPTIONAL_PARAMS = {
        "response_times": "1",
        "response_times_limit": "1",
        "logs": "1",
        "logs_limit": "1"
    }

    def __init__(self, api_key: str) -> None:
        """Create a collector

        Args:
            api_key (str): The Uptimerobot's API key
        """

        self._api_wrapper = UptimerobotReadApi(api_key)

    def collect(self) -> None:
        """Start the collection"""

        start = time.time()
        logging.info('Starting scraping at ' + str(start))

        try:
            status, monitors = self._api_wrapper.get_monitors(self.API_OPTIONAL_PARAMS)

            if not status:
                raise RequestException('Unable to get monitors from the API.')

            logging.debug('Got monitors informations from Uptimerobot API')

            for monitor in monitors:
                self.export_monitor(monitor)

            self.METRICS["up"].set(1)
        except RequestException as e:
            logging.error(e)
            self.METRICS["up"].set(0)

        duration_ms = (time.time() - start) * 1000
        self.METRICS["scrape_duration_milliseconds"].set(duration_ms)
        logging.info(f"Scrape complete in {duration_ms} milliseconds")

    def export_monitor(self, monitor: dict) -> None:
        """Export a monitor's metrics

        Args:
            monitor (dict): The monitor data returned from the API.
        """

        logging.debug(f'Exporting {monitor["friendly_name"]} metrics')

        # Status
        if "status" in monitor:
            self.METRICS["monitor_status"].labels(id=monitor["id"], url=monitor["url"], name=monitor[
            "friendly_name"], type=monitor["type"]).set(monitor["status"])

        # Last response time
        if len(monitor["response_times"]) > 0:
            self.METRICS["monitor_response_time"].labels(id=monitor["id"], url=monitor["url"], name=monitor[
                "friendly_name"], type=monitor["type"], status=monitor["status"]).set(monitor["response_times"][0]["value"])

        # Average response time
        if "average_response_time" in monitor:
            self.METRICS["monitor_response_time_average"].labels(id=monitor["id"], url=monitor["url"], name=monitor[
            "friendly_name"], type=monitor["type"]).set(monitor["average_response_time"])

        # Log type
        if len(monitor["logs"]) > 0:
            self.METRICS["monitor_log_type"].labels(id=monitor["id"], url=monitor["url"], name=monitor[
            "friendly_name"], type=monitor["type"]).set(monitor["logs"][0]["type"])

        # Log datetime
        if len(monitor["logs"]) > 0:
            self.METRICS["monitor_log_datetime"].labels(id=monitor["id"], url=monitor["url"], name=monitor[
            "friendly_name"], type=monitor["type"], logtype=monitor["logs"][0]["type"]).set(monitor["logs"][0]["datetime"])
