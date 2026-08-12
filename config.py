import os

from dotenv import load_dotenv


load_dotenv()


class Config:

    WEATHER_API_URL = os.getenv(
        "WEATHER_API_URL",
        "https://api.open-meteo.com/v1/forecast"
    )

    GEOCODING_API_URL = os.getenv(
        "GEOCODING_API_URL",
        "https://geocoding-api.open-meteo.com/v1/search"
    )

    REQUEST_TIMEOUT = int(
        os.getenv("REQUEST_TIMEOUT", "5")
    )