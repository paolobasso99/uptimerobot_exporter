import logging
import os
import typing
from dotenv import load_dotenv


class Settings:
    """Setting wrapper class
    This class is used to load envirorment variables and serve them.

    Attributes:
        LOG_LEVELS (dict): The possible log levels.
        defaults (dict): The default settings passed as a parameter to the constructor.
    """

    LOG_LEVELS = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    def __init__(self, defaults: dict) -> None:
        """Create a Settings instance

        Args:
            defaults (dict): The default settings.
        """

        # Set current settings as defaults
        self.defaults = defaults
        self.reset_defaults()

        # Load envirorment variables
        self.load_env()

    def set(self, name: str, value: typing.Any) -> None:
        """Set a setting by name and value

        Args:
            name (str): The name of the setting.
            value (Any): The calue of the setting.
        """

        self._current_settings[name] = value

    def get(self, name: str) -> typing.Any:
        """Get a setting by name

        Args:
            name (str): The name of the setting.

        Returns: 
            Any: The value of the setting. 
        """

        return self._current_settings[name]

    def reset_defaults(self) -> None:
        """Reset settings to the default values"""
        self._current_settings = self.defaults

    def load_env(self) -> None:
        """Load envirorment variables

        Raises:
            ValueError: If UPTIMEROBOT_READ_API_KEY env var is not set.
        """

        logging.debug("Loading envirorment variables")

        # Load .env
        load_dotenv()

        # LOG_LEVEL
        self.process_log_level()

        # UPTIMEROBOT_READ_API_KEY
        self.process_uptimerobot_read_api_key()

        # PORT
        self.process_port()

        # INTERVAL_SECONDS
        self.process_interval_seconds()

        logging.debug("Envirorment variables loaded")
        

    def process_uptimerobot_read_api_key(self) -> None:
        """Load and check UPTIMEROBOT_READ_API_KEY envirorment variable

        Raises:
            ValueError: If UPTIMEROBOT_READ_API_KEY env var is not set.
        """

        if "UPTIMEROBOT_READ_API_KEY" in os.environ and len(os.getenv("UPTIMEROBOT_READ_API_KEY")) > 0:
            self.set("UPTIMEROBOT_READ_API_KEY",
                     os.getenv("UPTIMEROBOT_READ_API_KEY"))
        else:
            raise ValueError(
                'UPTIMEROBOT_READ_API_KEY envirorment variable is not set.')

    def process_port(self) -> None:
        """Load and check PORT envirorment variable"""

        if "PORT" in os.environ:
            try:
                port = int(os.getenv("PORT"))
                if port <= 0:
                    raise ValueError("PORT must be a positive integer")
            except ValueError as e:
                logging.error(e)
                logging.error("Fallback to the default PORT=8000")
                port = 8000

            self.set("PORT", port)

    def process_interval_seconds(self) -> None:
        """Load and check INTERVAL_SECONDS envirorment variable"""

        if "INTERVAL_SECONDS" in os.environ:
            try:
                interval = int(os.getenv("INTERVAL_SECONDS"))
                if interval <= 0:
                    raise ValueError(
                        "INTERVAL_SECONDS must be a positive integer")
            except ValueError as e:
                logging.error(e)
                logging.error("Fallback to the default INTERVAL_SECONDS=300")
                interval = 300

            self.set("INTERVAL_SECONDS", interval)

    def process_log_level(self) -> None:
        """Load and check LOG_LEVEL envirorment variable"""
        
        log_level = "INFO"

        if "LOG_LEVEL" in os.environ:
            if os.getenv("LOG_LEVEL") in self.LOG_LEVELS:
                log_level = os.getenv("LOG_LEVEL")
            else:
                logging.warn(
                    f'{os.getenv("LOG_LEVEL")} is not a valid LOG_LEVEL, please pick between: DEBUG, INFO, WARN, ERROR, CRITICAL')
                logging.warn('Fallback to default LOG_LEVEL=INFO')
                log_level = "INFO"

            self.set("LOG_LEVEL", log_level)

        logging.getLogger().setLevel(self.LOG_LEVELS[log_level])