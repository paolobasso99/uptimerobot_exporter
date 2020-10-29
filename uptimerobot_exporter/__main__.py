"""uptimerobot_exporter entrypoint
This is the main entrypoint used to run uptimerobot_exporter.
"""

import logging
import time

from prometheus_client import start_http_server

from .banner import display_banner
from .settings import Settings
from .collector import UptimerobotCollector


def start_uptimerobot_exporter() -> None:
    """Start uptimerobot_exporter"""

    display_banner()

    # Load settings
    settings = Settings()

    logging.info(
        "uptimerobot_exporter version 0.0.1 by https://github.com/paolobasso99")
    logging.info("Initializated uptimerobot_exporter with:")
    logging.info("UPTIMEROBOT_READ_API_KEY=<redacted>")
    logging.info("LOG_LEVEL=" + settings.get("LOG_LEVEL"))
    logging.info("PORT=" + str(settings.get("PORT")))
    logging.info("INTERVAL_SECONDS=" + str(settings.get("INTERVAL_SECONDS")))

    # Create collector instance
    collector = UptimerobotCollector(settings.get("UPTIMEROBOT_READ_API_KEY"))

    # Start up the server to expose the metrics.
    start_http_server(settings.get("PORT"))
    logging.info(f'Metrics served at http://localhost:{settings.get("PORT")}')

    # Collect
    while True:
        collector.collect()
        logging.debug("Waiting " + str(settings.get("INTERVAL_SECONDS")) + " seconds before the next scrape")
        time.sleep(settings.get("INTERVAL_SECONDS"))

if __name__ == '__main__':
    start_uptimerobot_exporter()
