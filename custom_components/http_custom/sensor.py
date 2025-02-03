"""Sensor platform for esxi_stats."""
import logging

from homeassistant.helpers.entity import Entity
from .const import SENSOR_NAME


_LOGGER = logging.getLogger(__name__)


class HttpSwitchSensor(Entity):
    def __init__(self):
        self._state = None
        self._name = SENSOR_NAME

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_update(self):
        if self._state == 'open':
            self._state = 'close'
        else:
            self._state = 'open'
