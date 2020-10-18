import time
import logging
from prometheus_client import Gauge
from requests import RequestException
from UptimeRobotReadApi import UptimeRobotReadApi

# Define metrics
up = Gauge('uptimerobot_up',
           'The last scrape was successful')
scrape_duration_seconds = Gauge('uptimerobot_scrape_duration_seconds',
                                'The duration of the last scrape in seconds')

monitor_status = Gauge('uptimerobot_monitor_status',
                       'Status of the monitor: 0 = paused, 1 = not checked, 2 = up, 8 = seems down, 9 = down',
                       ['id', 'url', 'name', 'type'])

monitor_response_time = Gauge('uptimerobot_monitor_response_time_millisecond',
                              'Last response time of the monitor in milliseconds',
                              ['id', 'url', 'name', 'type', 'status'])

monitor_response_time_average = Gauge('uptimerobot_monitor_response_time_average_milliseconds',
                                      'Average response time of the monitor in milliseconds',
                                      ['id', 'url', 'name', 'type'])

monitor_log_type = Gauge('uptimerobot_monitor_log_type',
                         'Last log type of the monitor: 1 = down, 2 = up, 98 = started, 99 = paused',
                         ['id', 'url', 'name', 'type'])

monitor_log_datetime = Gauge('uptimerobot_monitor_log_datetime',
                             'Last log of the monitor datetime',
                             ['id', 'url', 'name', 'type', 'logtype'])

class UptimeRobotCollector():
    def __init__(self, api_key):
        self.api = UptimeRobotReadApi(api_key)

    def collect(self):
        start = time.time()
        logging.info('Starting scraping at ' + str(start))

        try:
            status, monitors = self.api.get_monitors(
                response_times=True, response_times_limit=1, logs=True, logs_limit=1, all_time_uptime_ratio=False)

            if not status:
                raise RequestException(monitors)
            else:
                logging.debug('Got monitors informations from Uptimerobot API')

            for monitor in monitors:
                logging.debug(f'Exporting {monitor["friendly_name"]} metrics')

                # Default metrics value
                status = 9
                response_time = 0
                response_time_average = 0
                log_type = 0
                log_datetime = 0

                # Status
                if "status" in monitor:
                    status = monitor["status"]

                monitor_status.labels(id=monitor["id"], url=monitor["url"], name=monitor[
                    "friendly_name"], type=monitor["type"]).set(status)

                # Last response time
                if len(monitor["response_times"]) > 0:
                    response_time = monitor["response_times"][0]["value"]

                monitor_response_time.labels(id=monitor["id"], url=monitor["url"], name=monitor[
                    "friendly_name"], type=monitor["type"], status=monitor["status"]).set(response_time)

                # Average response time
                if "average_response_time" in monitor:
                    response_time_average = monitor["average_response_time"]

                monitor_response_time_average.labels(id=monitor["id"], url=monitor["url"], name=monitor[
                    "friendly_name"], type=monitor["type"]).set(response_time_average)

                # Log type
                if len(monitor["logs"]) > 0:
                    log_type = monitor["logs"][0]["type"]

                monitor_log_type.labels(id=monitor["id"], url=monitor["url"], name=monitor[
                    "friendly_name"], type=monitor["type"]).set(log_type)

                # Log datetime
                if len(monitor["logs"]) > 0:
                    log_datetime = monitor["logs"][0]["datetime"]

                monitor_log_datetime.labels(id=monitor["id"], url=monitor["url"], name=monitor[
                    "friendly_name"], type=monitor["type"], logtype=monitor["logs"][0]["type"]).set(log_datetime)

            up.set(1)
        except RequestException as e:
            logging.error(e)
            up.set(0)

        duration = time.time() - start
        scrape_duration_seconds.set(duration)
        logging.info(f"Scrape complete in {duration} seconds")