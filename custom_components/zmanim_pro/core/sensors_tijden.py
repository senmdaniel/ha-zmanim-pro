import logging
from homeassistant.helpers.entity import Entity
import homeassistant.util.dt as dt_util

from .const import DOMAIN
# IMPORT AANGEPAST NAAR JOUW CORE MAP:
from .core_calculations import calculate_zmanim

_LOGGER = logging.getLogger(__name__)

class ZmanimTimeSensor(Entity):
    """Generieke sensor voor een specifieke gebedstijd (Zman)."""

    def __init__(self, provider, zman_key, sensor_name, icon, sub_key=None):
        self.provider = provider
        self._zman_key = zman_key
        self._sub_key = sub_key
        self._name = f"Zmanim Pro {sensor_name}"
        self._state = None
        self._icon = icon

    @property
    def name(self): return self._name
    @property
    def unique_id(self): 
        sub = f"_{self._sub_key}" if self._sub_key else ""
        return f"{DOMAIN}_{self._zman_key}{sub}"
    @property
    def state(self): return self._state
    @property
    def icon(self): return self._icon

    def update(self):
        """Bereken de tijden live via jouw core engine."""
        try:
            current_date = self.provider.get_current_date()
            config = {
                "timezone": str(dt_util.DEFAULT_TIME_ZONE),
                "latitude": self.hass.config.latitude,
                "longitude": self.hass.config.longitude,
                "city": self.hass.config.location_name
            }

            resultaat = calculate_zmanim(config, current_date)
            zmanim_data = resultaat["zmanim"]["zmanim"]

            if self._sub_key:
                self._state = zmanim_data[self._zman_key][self._sub_key]["time"]
            else:
                self._state = zmanim_data[self._zman_key]["time"]
        except Exception as e:
            _LOGGER.error("Fout bij berekenen van tijd %s: %s", self._name, e)
            self._state = "Fout"
