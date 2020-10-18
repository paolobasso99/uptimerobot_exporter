"""uptimerobot_exporter entrypoint
This is the main entrypoint used to run uptimerobot_exporter.
"""

import time
import logging
from prometheus_client import start_http_server
from UptimeRobotCollector import UptimeRobotCollector
from banner import display_banner
from Settings import Settings

DEFAULT_SETTINGS = {
    "PORT": 8000,
    "INTERVAL_SECONDS": 300,
    "LOG_LEVEL": "INFO"
}

if __name__ == '__main__':
    display_banner()

    # Load settings
    settings = Settings(DEFAULT_SETTINGS)

    logging.info(
        "uptimerobot_exporter version 0.0.1 by https://github.com/paolobasso99")
    logging.info("Initializated uptimerobot_exporter with:")
    logging.info("UPTIMEROBOT_READ_API_KEY=<redacted>")
    logging.info("LOG_LEVEL=" + settings.get("LOG_LEVEL"))
    logging.info("PORT=" + str(settings.get("PORT")))
    logging.info("INTERVAL_SECONDS=" + str(settings.get("INTERVAL_SECONDS")))
    logging.info(f'Access http://localhost:{settings.get("PORT")}')

    # Create collector instance
    collector = UptimeRobotCollector(settings.get("UPTIMEROBOT_READ_API_KEY"))

    # Start up the server to expose the metrics.
    start_http_server(settings.get("PORT"))

    # Collects
    while True:
        collector.collect()
        time.sleep(settings.get("INTERVAL_SECONDS"))
