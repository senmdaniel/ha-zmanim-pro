from .panel import async_setup_panel

async def async_setup(hass, config):
    hass.async_create_task(async_setup_panel(hass))
    return True
