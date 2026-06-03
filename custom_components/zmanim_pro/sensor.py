from datetime import timedelta
from homeassistant.helpers.entity import Entity

# Importeer je eigen DateProvider
from .date_provider import DateProvider

# Importeer de sensoren uit de aparte bestanden
from .sensors_data import GregorianDateSensor, JewishDateSensor
# (Straks voegen we hier sensors_tijden en sensors_feestdagen aan toe!)

# Update de sensoren elke 30 minuten
SCAN_INTERVAL = timedelta(minutes=30)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Zet alle Zmanim Pro sensoren klaar."""
    provider = DateProvider()
    
    # Hier verzamelen we alle sensoren uit de losse bestanden
    lijst_van_sensoren = [
        GregorianDateSensor(provider),
        JewishDateSensor(provider)
    ]
    
    # Geef de hele lijst in één keer aan Home Assistant
    async_add_entities(lijst_van_sensoren, True)
