import random
import time
import os
import logging
from prometheus_client import start_http_server
from dotenv import load_dotenv
from UptimeRobotCollector import UptimeRobotCollector
from banner import display_banner

if __name__ == '__main__':
    display_banner()

    # Load and check envirorment variables
    load_dotenv()

    if "UPTIMEROBOT_READ_API_KEY" not in os.environ:
        raise ValueError(
            'UPTIMEROBOT_READ_API_KEY envirorment variable is not set.')

    INTERVAL_SECONDS = 300
    if "INTERVAL_SECONDS" in os.environ:
        INTERVAL_SECONDS = int(os.getenv("INTERVAL_SECONDS"))

    # Set up logging
    level = logging.DEBUG
    levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    if "LOG_LEVEL" in os.environ and os.getenv("LOG_LEVEL") in levels:
        level = levels[os.getenv("LOG_LEVEL")]

    logging.getLogger().setLevel(level)

    logging.info(
        "uptimerobot_exporter version 0.0.1 by https://github.com/paolobasso99")
    logging.info("Initializated uptimerobot_exporter with:")
    logging.info("LOG_LEVEL="+os.getenv("LOG_LEVEL"))
    logging.info("INTERVAL_SECONDS="+os.getenv("INTERVAL_SECONDS"))

    # Create collector instance
    collector = UptimeRobotCollector(os.getenv("UPTIMEROBOT_READ_API_KEY"))

    # Start up the server to expose the metrics.
    start_http_server(8000)

    # Collect
    while True:
        collector.collect()
        time.sleep(INTERVAL_SECONDS)
