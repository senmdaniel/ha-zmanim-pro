from homeassistant.components import frontend

async def async_setup_panel(hass):
    frontend.async_register_built_in_panel(
        hass,
        component_name="iframe",
        sidebar_title="Hello World",
        sidebar_icon="mdi:web",
        frontend_url_path="hello-world",
        config={
            "url": "https://senmdaniel.github.io/ha-hello-world-/"
        },
    )
    
