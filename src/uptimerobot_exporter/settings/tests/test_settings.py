import unittest
import os
from uptimerobot_exporter.settings.settings import Settings


class SettingsTest(unittest.TestCase):

    def setUp(self):
        os.environ["LOG_LEVEL"] = "CRITICAL"
        os.environ["INTERVAL_SECONDS"] = "200"
        os.environ["PORT"] = "8080"
        os.environ["UPTIMEROBOT_READ_API_KEY"] = "api-keey"

    def test_defaults(self):
        settings = Settings()
        settings.DEFAULT = {
            "PORT": 1111,
            "INTERVAL_SECONDS": 600,
            "LOG_LEVEL": "CRITICAL"
        }
        settings.reset_default()

        self.assertEqual(settings.get("LOG_LEVEL"), "CRITICAL", "Should be CRITICAL")
        self.assertEqual(settings.get("INTERVAL_SECONDS"), 600, "Should be 200")
        self.assertEqual(settings.get("PORT"), 1111, "Should be 8080")
        self.assertEqual(settings.get("UPTIMEROBOT_READ_API_KEY"), "api-keey", "Should be api-keey")

    def test_env(self):
        settings = Settings()
        self.assertEqual(settings.get("LOG_LEVEL"), "CRITICAL", "Should be CRITICAL")
        self.assertEqual(settings.get("INTERVAL_SECONDS"), 200, "Should be 200")
        self.assertEqual(settings.get("PORT"), 8080, "Should be 8080")
        self.assertEqual(settings.get("UPTIMEROBOT_READ_API_KEY"), "api-keey", "Should be api-keey")

if __name__ == '__main__':
    unittest.main()
