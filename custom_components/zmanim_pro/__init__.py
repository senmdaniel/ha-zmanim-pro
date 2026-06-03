import logging
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant
from .date_provider import DateProvider
from .core_calculations import calculate_zmanim
import homeassistant.util.dt as dt_util

_LOGGER = logging.getLogger(__name__)
DOMAIN = "zmanim_pro"

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Zet de Zmanim Pro integratie en de API-view klaar."""
    # Registreer de browser-link bij Home Assistant
    hass.http.register_view(ZmanimApiView(hass))
    return True

class ZmanimApiView(HomeAssistantView):
    """Maakt een onbeveiligde API-pagina aan in de browser."""
    url = "/api/zmanim"
    name = "api:zmanim"
    requires_auth = False  # Dit voorkomt de 401 foutmelding!

    def __init__(self, hass: HomeAssistant):
        self.hass = hass
        self.provider = DateProvider()

    def get(self, request):
        """Dit wordt uitgevoerd als je de link opent in je browser."""
        try:
            current_date = self.provider.get_current_date()
            
            # Haal live locatiegegevens uit Home Assistant
            config_data = {
                "timezone": str(dt_util.DEFAULT_TIME_ZONE),
                "latitude": self.hass.config.latitude,
                "longitude": self.hass.config.longitude,
                "city": self.hass.config.location_name
            }

            # Bereken de tijden via jouw core engine
            zmanim_output = calculate_zmanim(config_data, current_date)
            
            # Bouw de JSON exact zo op als jouw Pi deed!
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
