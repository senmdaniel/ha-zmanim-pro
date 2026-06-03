import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
import homeassistant.util.dt as dt_util

from .date_provider import DateProvider
from .core_calculations import calculate_zmanim
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Vertel Home Assistant dat we SENSOR-entiteiten hebben
PLATFORMS = [Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Zet de integratie klaar via een UI Config Entry."""
    # Registreer direct de onbeveiligde browser-link
    hass.http.register_view(ZmanimApiView(hass))
    
    # Start de sensoren op (dit vervangt de oude configuration.yaml methode)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Zorg voor een schone afsluiting als de integratie wordt verwijderd."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


class ZmanimApiView(HomeAssistantView):
    """Maakt de onbeveiligde API-pagina aan in de browser op /api/zmanim."""
    url = "/api/zmanim"
    name = "api:zmanim"
    requires_auth = False

    def __init__(self, hass: HomeAssistant):
        self.hass = hass
        self.provider = DateProvider()

    def get(self, request):
        try:
            current_date = self.provider.get_current_date()
            config_data = {
                "timezone": str(dt_util.DEFAULT_TIME_ZONE),
                "latitude": self.hass.config.latitude,
                "longitude": self.hass.config.longitude,
                "city": self.hass.config.location_name
            }

            zmanim_output = calculate_zmanim(config_data, current_date)
            
            return self.json({
                "status": "ok",
                "date": str(current_date),
                "hebrew": {
                    "hebrew_day": self.provider.get_current_jewish_day(),
                    "hebrew_month": self.provider.get_current_jewish_month(),
                    "hebrew_date_string": self.provider.get_jewish_date_string()
                },
                "zmanim": zmanim_output["zmanim"]
            })
        except Exception as e:
            _LOGGER.error("API Fout: %s", e)
            return self.json({"status": "error", "message": str(e)}, 500)
