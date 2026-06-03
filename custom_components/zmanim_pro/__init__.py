import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.components import webhook
from aiohttp import web
import homeassistant.util.dt as dt_util

from .date_provider import DateProvider
from .core.core_calculations import calculate_zmanim

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Dit start de integratie op zodra hij in de UI is toegevoegd."""
    
    # Registreer een unieke, onbeveiligde webhook URL
    webhook.async_register(
        hass,
        "zmanim_pro",                    # De domeinnaam
        "zmanim_api_webhook",            # Een unieke ID voor de route
        handle_webhook_request           # De functie die de JSON bouwt
    )
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def handle_webhook_request(hass: HomeAssistant, webhook_id: str, request) -> web.Response:
    """Dit wordt direct asynchroon uitgevoerd als je de link opent."""
    try:
        provider = DateProvider()
        current_date = provider.get_current_date()
        
        config_data = {
            "timezone": str(dt_util.DEFAULT_TIME_ZONE),
            "latitude": hass.config.latitude,
            "longitude": hass.config.longitude,
            "city": hass.config.location_name
        }

        zmanim_output = calculate_zmanim(config_data, current_date)
        
        data = {
            "status": "ok",
            "date": str(current_date),
            "hebrew": {
                "hebrew_day": provider.get_current_jewish_day(),
                "hebrew_month": provider.get_current_jewish_month(),
                "hebrew_date_string": provider.get_jewish_date_string()
            },
            "zmanim": zmanim_output["zmanim"]
        }
        return web.json_response(data)

    except Exception as e:
        _LOGGER.error("Webhook API Fout: %s", e)
        return web.json_response({"status": "error", "message": str(e)}, status=500)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Zorg voor een schone afsluiting en verwijder de webhook."""
    webhook.async_unregister(hass, "zmanim_api_webhook")
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
