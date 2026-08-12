from services.weather_service import (
    WeatherService
)


def test_weather_condition():

    service = WeatherService()

    condition, icon = (
        service.get_weather_condition(0)
    )

    assert condition == "Clear Sky"

    assert icon == "☀️"


def test_unknown_weather_condition():

    service = WeatherService()

    condition, icon = (
        service.get_weather_condition(999)
    )

    assert condition == "Unknown"

    assert icon == "🌍"


def test_forecast_date_today():

    service = WeatherService()

    result = service.format_forecast_date(
        "2026-08-17",
        0
    )

    assert result == "TODAY"


def test_forecast_date_weekday():

    service = WeatherService()

    result = service.format_forecast_date(
        "2026-08-18",
        1
    )

    assert result == "Tue"