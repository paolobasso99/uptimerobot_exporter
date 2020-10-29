import logging
import os
import typing

from dotenv import load_dotenv


class Settings:
    """Setting wrapper class
    This class is used to load envirorment variables and serve them.

    Attributes:
        LOG_LEVELS (dict): The possible log levels.
        DEFAULT (dict): The default settings.
    """

    DEFAULT = {
        "PORT": 8000,
        "INTERVAL_SECONDS": 300,
        "LOG_LEVEL": "INFO"
    }

    LOG_LEVELS = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    def __init__(self) -> None:
        """Create a Settings instance

        Args:
            defaults (dict): The default settings.
        """

        self._current_settings = {}

        # Set current settings as defaults
        self.reset_default()

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

    def reset_default(self) -> None:
        """Reset settings to the default values"""

        self._current_settings.update(self.DEFAULT)

    def load_env(self) -> None:
        """Load envirorment variables

        Raises:
            ValueError: If UPTIMEROBOT_READ_API_KEY env var is not set.
        """

        logging.debug("Loading envirorment variables")

        # Load .env
        load_dotenv()

        # LOG_LEVEL
        self.load_log_level()

        # UPTIMEROBOT_READ_API_KEY
        self.load_uptimerobot_read_api_key()

        # PORT
        self.load_port()

        # INTERVAL_SECONDS
        self.load_interval_seconds()

        logging.debug("Envirorment variables loaded")
        

    def load_uptimerobot_read_api_key(self) -> None:
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

    def load_port(self) -> None:
        """Load and check PORT envirorment variable

        Raises:
            ValueError: If PORT env var is not a positive integer.
        """

        if "PORT" in os.environ:
            port = int(os.getenv("PORT"))
            if port <= 0:
                raise ValueError("PORT must be a positive integer")

            self.set("PORT", port)

    def load_interval_seconds(self) -> None:
        """Load and check INTERVAL_SECONDS envirorment variable

        Raises:
            ValueError: If INTERVAL_SECONDS env var is not a positive integer.
        """

        if "INTERVAL_SECONDS" in os.environ:
            interval = int(os.getenv("INTERVAL_SECONDS"))
            if interval <= 0:
                raise ValueError(
                    "INTERVAL_SECONDS must be a positive integer")

            self.set("INTERVAL_SECONDS", interval)

    def load_log_level(self) -> None:
        """Load and check LOG_LEVEL envirorment variable"""
        
        log_level = "INFO"

        if "LOG_LEVEL" in os.environ:
            if os.getenv("LOG_LEVEL") in self.LOG_LEVELS:
                log_level = os.getenv("LOG_LEVEL")
            else:
                logging.warning(
                    f'{os.getenv("LOG_LEVEL")} is not a valid LOG_LEVEL, please pick between: DEBUG, INFO, WARN, ERROR, CRITICAL')
                logging.warning('Fallback to default LOG_LEVEL=INFO')
                log_level = "INFO"

            self.set("LOG_LEVEL", log_level)

        logging.getLogger().setLevel(self.LOG_LEVELS[log_level])
