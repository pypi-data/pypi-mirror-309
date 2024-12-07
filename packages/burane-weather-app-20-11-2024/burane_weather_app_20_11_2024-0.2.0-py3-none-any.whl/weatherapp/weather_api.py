import requests
from datetime import date, timedelta
from model.historical_response import HistoricalResponse
from model.historical_request import HistoricalWeatherParam
from model.forecast_request import CurrentEnum, ForecastWeatherParam
from model.forecast_response import ForecastResponse


class WeatherApi:
    API_URL = "https://api.open-meteo.com/v1/"
    FORECAST = "forecast"
    ARCHIVE_API_URL = "https://archive-api.open-meteo.com/v1/"
    HISTORICAL = "archive"

    def __init__(self) -> None:
        pass

    def get_forecast(self, params: ForecastWeatherParam) -> ForecastResponse:

        query_params = {
            "latitude": params.lattitude,
            "longitude": params.longitude,
            "current": ",".join([e.value for e in params.current]),
        }

        res = requests.get(f"{self.API_URL}{self.FORECAST}", params=query_params).json()
        return ForecastResponse.from_dict(res)

    def get_historical(self, params: HistoricalWeatherParam) -> HistoricalResponse:

        query_params = {
            "latitude": params.lattitude,
            "longitude": params.longitude,
            "hourly": ",".join([e.value for e in params.hourly]),
            "start_date": params.start_date,
            "end_date": params.end_date,
        }

        res = requests.get(f"{self.ARCHIVE_API_URL}{self.HISTORICAL}", params=query_params).json()
        return HistoricalResponse.from_dict(res)


# caen = (49.183, -0.38)
# w = WeatherApi()
# today = date.today() - timedelta(weeks=1)
# yesterday = today - timedelta(days=1, weeks=1)
# param = HistoricalWeatherParam(
#     lattitude=caen[0],
#     longitude=caen[1],
#     start_date=yesterday,
#     end_date=yesterday,
#     hourly=[
#         CurrentEnum.RELATIVE_HUMIDITY_2m,
#         CurrentEnum.TEMP_2M,
#         CurrentEnum.WIND_SPEED_2M,
#     ],
# )
# w.get_historical(params=param)
