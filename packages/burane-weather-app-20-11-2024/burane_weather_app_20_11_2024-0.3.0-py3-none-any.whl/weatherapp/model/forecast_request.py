from dataclasses import dataclass
from enum import Enum

class CurrentEnum(Enum):
    TEMP_2M = "temperature_2m"
    WIND_SPEED_2M = "wind_speed_10m"
    RELATIVE_HUMIDITY_2m = "relative_humidity_2m"
        
@dataclass
class ForecastWeatherParam:
    lattitude: float
    longitude: float
    current: list[CurrentEnum]
    