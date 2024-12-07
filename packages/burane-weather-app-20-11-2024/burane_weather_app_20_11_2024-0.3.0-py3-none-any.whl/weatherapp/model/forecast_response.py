from dataclasses import dataclass
from datetime import datetime

from typing import Any
from dataclasses import dataclass


@dataclass
class Current:
    time: datetime
    interval: int
    relative_humidity_2m: int
    temperature_2m: float
    wind_speed_10m: float

    @staticmethod
    def from_dict(obj: Any) -> 'Current':
        _time = str(obj.get("time"))
        _interval = int(obj.get("interval"))
        _relative_humidity_2m = int(obj.get("relative_humidity_2m"))
        _temperature_2m = float(obj.get("temperature_2m"))
        _wind_speed_10m = float(obj.get("wind_speed_10m"))
        return Current(_time, _interval, _relative_humidity_2m, _temperature_2m, _wind_speed_10m)

@dataclass
class CurrentUnits:
    time: str
    interval: str
    relative_humidity_2m: str
    temperature_2m: str
    wind_speed_10m: str

    @staticmethod
    def from_dict(obj: Any) -> 'CurrentUnits':
        _time = str(obj.get("time"))
        _interval = str(obj.get("interval"))
        _relative_humidity_2m = str(obj.get("relative_humidity_2m"))
        _temperature_2m = str(obj.get("temperature_2m"))
        _wind_speed_10m = str(obj.get("wind_speed_10m"))
        return CurrentUnits(_time, _interval, _relative_humidity_2m, _temperature_2m, _wind_speed_10m)

@dataclass
class ForecastResponse:
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    current_units: CurrentUnits
    current: Current

    @staticmethod
    def from_dict(obj: Any) -> 'ForecastResponse':
        _latitude = float(obj.get("latitude"))
        _longitude = float(obj.get("longitude"))
        _generationtime_ms = float(obj.get("generationtime_ms"))
        _utc_offset_seconds = int(obj.get("utc_offset_seconds"))
        _timezone = str(obj.get("timezone"))
        _timezone_abbreviation = str(obj.get("timezone_abbreviation"))
        _elevation = float(obj.get("elevation"))
        _current_units = CurrentUnits.from_dict(obj.get("current_units"))
        _current = Current.from_dict(obj.get("current"))
        return ForecastResponse(_latitude, _longitude, _generationtime_ms, _utc_offset_seconds, _timezone, _timezone_abbreviation, _elevation, _current_units, _current)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
