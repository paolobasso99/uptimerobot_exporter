"""uptimerobot_exporter entrypoint
This is the main entrypoint used to run uptimerobot_exporter.
"""

import time
import logging
from prometheus_client import start_http_server
from uptimerobot_collector.uptimerobot_collector import UptimerobotCollector
from banner import display_banner
from settings.settings import Settings

if __name__ == '__main__':
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

    # Collects
    while True:
        collector.collect()
        time.sleep(settings.get("INTERVAL_SECONDS"))
