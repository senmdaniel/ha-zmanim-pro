from datetime import datetime
import json
import os
import pytz

# Importeer de berekeningslogica rechtstreeks uit jouw core map
from custom_components.zmanim_pro.core.core_calculations import calculate_zmanim

def main():
    # Locatiedata ophalen uit de GitHub omgevingsvariabelen
    config = {
        "timezone": os.getenv("TIMEZONE", "Europe/Amsterdam"),
        "latitude": os.getenv("LATITUDE", "52.3676"),
        "longitude": os.getenv("LONGITUDE", "4.9041"),
        "city": os.getenv("CITY", "Home")
    }

    tz = pytz.timezone(config["timezone"])
    current_date = datetime.now(tz).date()

    # Bereken de Zmanim via jouw eigen engine
    raw_result = calculate_zmanim(config, current_date)
    zmanim = raw_result["zmanim"]["zmanim"]
    shabbat = raw_result["zmanim"]["shabbat_options"]

    # Vlakke JSON structuur maken die Loxone perfect kan parsen
    loxone_output = {
        "datum": current_date.strftime("%Y%m%d"),
        "shkia_time": zmanim["shkia"]["time"],
        "shkia_ts": zmanim["shkia"]["ts"],
        "chatzos_time": zmanim["chatzos"]["time"],
        "chatzos_ts": zmanim["chatzos"]["ts"],
        "plag_gra_time": zmanim["plag_hamincha"]["pla_gra"]["time"],
        "plag_gra_ts": zmanim["plag_hamincha"]["pla_gra"]["ts"],
        "plag_ma_time": zmanim["plag_hamincha"]["plag_magen_avraham"]["time"],
        "plag_ma_ts": zmanim["plag_hamincha"]["plag_magen_avraham"]["ts"],
        "shema_gra_time": zmanim["sof_zman_krias_shema"]["gra"]["time"],
        "shema_gra_ts": zmanim["sof_zman_krias_shema"]["gra"]["ts"],
        "shema_ma_time": zmanim["sof_zman_krias_shema"]["magen_avraham"]["time"],
        "shema_ma_ts": zmanim["sof_zman_krias_shema"]["magen_avraham"]["ts"],
        "tefila_gra_time": zmanim["sof_zman_tefila"]["gra"]["time"],
        "tefila_gra_ts": zmanim["sof_zman_tefila"]["gra"]["ts"],
        "tefila_ma_time": zmanim["sof_zman_tefila"]["magen_avraham"]["time"],
        "tefila_ma_ts": zmanim["sof_zman_tefila"]["magen_avraham"]["ts"]
    }

    for option in shabbat["candle_lighting"]:
        loxone_output[f"{option['id']}_time"] = option["time"]
        loxone_output[f"{option['id']}_ts"] = option["ts"]

    for option in shabbat["tzeis"]:
        loxone_output[f"{option['id']}_time"] = option["time"]
        loxone_output[f"{option['id']}_ts"] = option["ts"]

    # Opslaan als zmanim.json
    with open("zmanim.json", "w") as f:
        json.dump(loxone_output, f, indent=2)
        
    print("Zmanim JSON succesvol gegenereerd!")

if __name__ == "__main__":
    main()
