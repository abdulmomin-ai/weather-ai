import logging
import os

from flask import (
    Flask,
    render_template,
    request
)

from services.weather_service import (
    WeatherService
)


os.makedirs("logs", exist_ok=True)


logging.basicConfig(

    level=logging.INFO,

    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),

    handlers=[

        logging.FileHandler(
            "logs/weatherai.log"
        ),

        logging.StreamHandler()
    ]
)


logger = logging.getLogger(__name__)


app = Flask(__name__)

weather_service = WeatherService()


@app.route("/", methods=["GET"])
def home():

    weather_data = None

    city = request.args.get(
        "city",
        ""
    ).strip()

    if city:

        logger.info(
            "Weather search requested: %s",
            city
        )

        try:

            weather_data = (
                weather_service
                .get_weather_by_city(city)
            )

            if weather_data is None:

                logger.warning(
                    "City not found: %s",
                    city
                )

        except Exception:

            logger.exception(
                "Unexpected error while "
                "processing city: %s",
                city
            )

    return render_template(
        "index.html",
        weather_data=weather_data,
        city=city
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )