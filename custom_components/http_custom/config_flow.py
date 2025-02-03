"""Adds config flow for ESXi Stats."""
import logging
from collections import OrderedDict
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    DOMAIN,
    CONF_HOST_NAME,
    CONF_HOST_STATA, DEFAULT_HOST_STATE, DEFAULT_HOST_PORT,
)
from .http import http_connect

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class HTTPSwitchLowHandler(config_entries.ConfigFlow):
    """Config flow for ESXi Stats."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return HttpSwitchOptionsFlow(config_entry)

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(
            self, user_input={}
    ):  # pylint: disable=dangerous-default-value
        """Handle a flow initialized by the user."""
        self._errors = {}
        if self.hass.data.get(DOMAIN):
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            # Check if entered host is already in HomeAssistant
            existing = await self._check_existing(user_input["host"])
            if existing:
                return self.async_abort(reason="already_configured")

            # If it is not, continue with communication test
            valid = await self.hass.async_add_executor_job(
                self._test_communication,
                user_input["host"],
                user_input["port"]
            )
            if valid:
                return self.async_create_entry(
                    title=user_input["host"], data=user_input
                )
            else:
                self._errors["base"] = "communication"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):
        """Show the configuration form to edit location data."""
        # Defaults
        host = ""
        port = DEFAULT_HOST_PORT

        if user_input is not None:
            if "host" in user_input:
                host = user_input["host"]
            if "port" in user_input:
                port = user_input["port"]

        data_schema = OrderedDict()
        data_schema[vol.Required("host", default=host)] = str
        data_schema[vol.Required("port", default=port)] = int
        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(data_schema), errors=self._errors
        )

    async def async_step_import(self, user_input):
        """Import a config entry.

        Special type of import, we're not actually going to store any data.
        Instead, we're going to rely on the values that are in config file.
        """
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        return self.async_create_entry(title="configuration.yaml", data={})

    async def _check_existing(self, host):
        for entry in self._async_current_entries():
            if host == entry.data.get("host"):
                return True

    def _test_communication(self, host, port, verify_ssl, username, password):
        """Return true if the communication is ok."""
        try:
            return http_connect(host, port)
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error(exception)
            return False


class HttpSwitchOptionsFlow(config_entries.OptionsFlow):
    """Handle Http Switch options."""

    def __init__(self, config_entry):
        """Initialize Http Switch options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):
        """Manage ESXi Stats options."""
        return await self.async_step_http_options()

    async def async_step_http_options(self, user_input=None):
        """Manage ESXi Stats Options."""
        if user_input is not None:
            self.options[CONF_HOST_NAME] = user_input[CONF_HOST_NAME]
            self.options[CONF_HOST_STATA] = user_input[CONF_HOST_STATA]
            return self.async_create_entry(title="", data=self.options)

        return self.async_show_form(
            step_id="http_options",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_HOST_STATA,
                        default=self.config_entry.options.get(
                            CONF_HOST_STATA, DEFAULT_HOST_STATE
                        ),
                    ): vol.In(CONF_HOST_STATA)
                }
            ),
        )
