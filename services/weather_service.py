from datetime import datetime
import requests
from config import Config


class WeatherService:

    def search_city(self, city):
        params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        response = requests.get(
            Config.GEOCODING_API_URL,
            params=params,
            timeout=Config.REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()
        results = data.get("results")

        if not results:
            return None

        location = results[0]

        return {
            "name": location["name"],
            "country": location.get("country", ""),
            "latitude": location["latitude"],
            "longitude": location["longitude"]
        }

    def format_forecast_date(self, date_string, index):
        """Convert API date into a user-friendly display format."""
        date_object = datetime.strptime(
            date_string,
            "%Y-%m-%d"
        )

        if index == 0:
            return "TODAY"

        return date_object.strftime("%a")

    def get_weather_condition(self, weather_code):
        conditions = {
            0: ("Clear Sky", "☀️"),
            1: ("Mainly Clear", "🌤️"),
            2: ("Partly Cloudy", "⛅"),
            3: ("Overcast", "☁️"),
            45: ("Fog", "🌫️"),
            48: ("Depositing Rime Fog", "🌫️"),
            51: ("Light Drizzle", "🌦️"),
            53: ("Moderate Drizzle", "🌦️"),
            55: ("Dense Drizzle", "🌧️"),
            61: ("Light Rain", "🌦️"),
            63: ("Moderate Rain", "🌧️"),
            65: ("Heavy Rain", "🌧️"),
            71: ("Light Snow", "🌨️"),
            73: ("Moderate Snow", "❄️"),
            75: ("Heavy Snow", "❄️"),
            80: ("Rain Showers", "🌦️"),
            81: ("Moderate Rain Showers", "🌧️"),
            82: ("Violent Rain Showers", "⛈️"),
            95: ("Thunderstorm", "⛈️")
        }

        return conditions.get(weather_code, ("Unknown", "🌍"))

    def get_current_weather(self, latitude, longitude):
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "wind_speed_10m,"
                "weather_code"
            ),
            "daily": (
                "weather_code,"
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_probability_max"
            ),
            "forecast_days": 7,
            "timezone": "auto"
        }

        response = requests.get(
            Config.WEATHER_API_URL,
            params=params,
            timeout=Config.REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        current = data["current"]
        daily = data["daily"]

        forecast = []

        # 1. 7-Day Forecast Loop
        for index in range(len(daily["time"])):
            condition_name, condition_icon = self.get_weather_condition(
                daily["weather_code"][index]
            )

            formatted_date = self.format_forecast_date(
                daily["time"][index],
                index
            )

            forecast.append({
                "date": formatted_date,
                "weather_code": daily["weather_code"][index],
                "condition": condition_name,
                "icon": condition_icon,
                "max_temp": daily["temperature_2m_max"][index],
                "min_temp": daily["temperature_2m_min"][index],
                "rain_probability": (
                    daily["precipitation_probability_max"][index]
                )
            })

        # 2. Live/Current weather condition extraction
        curr_condition_name, curr_condition_icon = self.get_weather_condition(
            current["weather_code"]
        )

        current_weather = {
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "wind_speed": current["wind_speed_10m"],
            "weather_code": current["weather_code"],
            "condition": curr_condition_name,
            "icon": curr_condition_icon
        }

        # 3. Final Return
        return {
            "current": current_weather,
            "forecast": forecast
        }

    def get_weather_by_city(self, city):
        location = self.search_city(city)

        if location is None:
            return None

        weather = self.get_current_weather(
            location["latitude"],
            location["longitude"]
        )

        return {
            "location": location,
            "weather": weather
        }