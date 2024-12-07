from datetime import date, datetime
from weatherapp.model.historical_response import HistoricalResponse
from weatherapp.model.historical_request import HistoricalWeatherParam
from weatherapp.model.forecast_response import ForecastResponse
from weatherapp.model.forecast_request import CurrentEnum, ForecastWeatherParam
from weatherapp.weather_api import WeatherApi
import time


class Weather:

    def __init__(self) -> None:
        self.weather_api = WeatherApi()

    def display_currrent_weather(
        self, lat: float, long: float, refresh_delay_second: float = 1
    ) -> None:
        if refresh_delay_second < 1:
            print("Refresh delay cant be less than 1, it will be set to 1")
            refresh_delay_second = 1

        params = ForecastWeatherParam(
            lattitude=lat,
            longitude=long,
            current=[
                CurrentEnum.RELATIVE_HUMIDITY_2m,
                CurrentEnum.TEMP_2M,
                CurrentEnum.WIND_SPEED_2M,
            ],
        )

        while True:
            forecast = self.weather_api.get_forecast(params=params)
            print(chr(27) + "[2J")
            print(self._format_forecast_(forecast))
            time.sleep(1)

    def display_past_weather(
        self, lat: float, long: float, start: datetime, stop: datetime
    ) -> None:
        now = date.today()
        if now < start or now < stop or stop < start:
            print("Bad dates")

        params = HistoricalWeatherParam(
            lattitude=lat,
            longitude=long,
            start_date=start,
            end_date=stop,
            hourly=[
                CurrentEnum.RELATIVE_HUMIDITY_2m,
                CurrentEnum.TEMP_2M,
                CurrentEnum.WIND_SPEED_2M,
            ],
        )

        historical_data = self.weather_api.get_historical(params=params)

        print(chr(27) + "[2J")
        print(self._format_historical_(historical_data))

    @staticmethod
    def _format_historical_(historical: HistoricalResponse) -> str:

        headers = ["Time", "Temperature", "Wind speed", "Relative humidity"]

        values = [
            historical.hourly.time,
            [
                f"{w}{historical.hourly_units.temperature_2m}"
                for w in historical.hourly.temperature_2m
            ],
            [
                f"{w}{historical.hourly_units.wind_speed_10m}"
                for w in historical.hourly.wind_speed_10m
            ],
            [
                f"{w}{historical.hourly_units.relative_humidity_2m}"
                for w in historical.hourly.relative_humidity_2m
            ],
        ]

        return Weather._format_table_(list(zip(headers, values)))

    @staticmethod
    def _format_forecast_(forecast: ForecastResponse) -> str:

        headers = ["Time", "Temperature", "Wind speed", "Relative humidity"]

        values = [
            [forecast.current.time],
            [
                f"{forecast.current.temperature_2m}{forecast.current_units.temperature_2m}"
            ],
            [
                f"{forecast.current.wind_speed_10m}{forecast.current_units.wind_speed_10m}"
            ],
            [
                f"{forecast.current.relative_humidity_2m}{forecast.current_units.relative_humidity_2m}"
            ],
        ]

        return Weather._format_table_(list(zip(headers, values)))

    @staticmethod
    def _format_table_(headers_values: list[(str, list[str])]) -> str:
        COL_WIDTH = 20
        BORDER_WIDTH = COL_WIDTH + 2

        NUM_COL = len(headers_values)

        top_border = f"┌{'┬'.join(['─' * BORDER_WIDTH for _ in range(NUM_COL)])}┐\n"
        separator = f"├{'┼'.join(['─' * BORDER_WIDTH for _ in range(NUM_COL)])}┤\n"
        bottom_border = f"└{'┴'.join(['─' * BORDER_WIDTH for _ in range(NUM_COL)])}┘\n"
        header = f"│{'│'.join([f' {header[0]:^{COL_WIDTH}} ' for header in headers_values])}│\n"

        data = []
        for i in range(len(headers_values[1][1])):
            values = [x[1][i] for x in headers_values]
            s = f"│{'│'.join( [f' {w:^{COL_WIDTH}} ' for w in values] )}│\n"
            data.append(s)

        return f"{top_border}{header}{separator}{''.join(data)}{bottom_border}"