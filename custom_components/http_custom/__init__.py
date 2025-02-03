from homeassistant.core import HomeAssistant
from homeassistant.helpers import discovery
from .const import DOMAIN


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Http Custom component."""
    # @TODO: Add setup code.
    hass.data[DOMAIN] = {}
    return True
