"""Constants for Http Switch."""

DOMAIN = "http_custom"
"""Constants for Http Switch."""
SENSOR_NAME = f"sensor_{DOMAIN}"
DOMAIN_DATA = f"{DOMAIN}_data"

PLATFORMS = ["sensor"]
REQUIRED_FILES = [
    "const.py",
    "http.py",
    "manifest.json",
    "sensor.py",
    "config_flow.py"
]
VERSION = "0.0.1"
ISSUE_URL = "https://github.com/wxt9861/esxi_stats/issues"
CONF_NAME = "name"
CONF_HOST_NAME = "hostname"
CONF_HOST_STATA = "hoststatus"
DEFAULT_HOST_PORT = 80
DEFAULT_HOST_STATE = "close"