import logging
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant
import homeassistant.util.dt as dt_util

from .date_provider import DateProvider
from .core.core_calculations import calculate_zmanim

_LOGGER = logging.getLogger(__name__)

def setup(hass: HomeAssistant, config: dict) -> bool:
    """Zet de Zmanim Pro API direct klaar bij het opstarten van HA."""
    hass.http.register_view(ZmanimApiView(hass))
    return True

class ZmanimApiView(HomeAssistantView):
    """Maakt de onbeveiligde API-pagina aan op /api/zmanim."""
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
