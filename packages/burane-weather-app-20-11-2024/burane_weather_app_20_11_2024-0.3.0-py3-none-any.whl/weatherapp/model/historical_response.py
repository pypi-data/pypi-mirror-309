from typing import List
from typing import Any
from dataclasses import dataclass


@dataclass
class Hourly:
    time: List[str]
    relative_humidity_2m: List[int]
    temperature_2m: List[float]
    wind_speed_10m: List[float]

    @staticmethod
    def from_dict(obj: Any) -> "Hourly":
        _time = [y for y in obj.get("time")]
        _relative_humidity_2m = [y for y in obj.get("relative_humidity_2m")]
        _temperature_2m = [y for y in obj.get("temperature_2m")]
        _wind_speed_10m = [y for y in obj.get("wind_speed_10m")]
        return Hourly(_time, _relative_humidity_2m, _temperature_2m, _wind_speed_10m)


@dataclass
class HourlyUnits:
    time: str
    relative_humidity_2m: str
    temperature_2m: str
    wind_speed_10m: str

    @staticmethod
    def from_dict(obj: Any) -> "HourlyUnits":
        _time = str(obj.get("time"))
        _relative_humidity_2m = str(obj.get("relative_humidity_2m"))
        _temperature_2m = str(obj.get("temperature_2m"))
        _wind_speed_10m = str(obj.get("wind_speed_10m"))
        return HourlyUnits(
            _time, _relative_humidity_2m, _temperature_2m, _wind_speed_10m
        )


@dataclass
class HistoricalResponse:
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    hourly_units: HourlyUnits
    hourly: Hourly

    @staticmethod
    def from_dict(obj: Any) -> "HistoricalResponse":
        _latitude = float(obj.get("latitude"))
        _longitude = float(obj.get("longitude"))
        _generationtime_ms = float(obj.get("generationtime_ms"))
        _utc_offset_seconds = int(obj.get("utc_offset_seconds"))
        _timezone = str(obj.get("timezone"))
        _timezone_abbreviation = str(obj.get("timezone_abbreviation"))
        _elevation = float(obj.get("elevation"))
        _hourly_units = HourlyUnits.from_dict(obj.get("hourly_units"))
        _hourly = Hourly.from_dict(obj.get("hourly"))
        return HistoricalResponse(
            _latitude,
            _longitude,
            _generationtime_ms,
            _utc_offset_seconds,
            _timezone,
            _timezone_abbreviation,
            _elevation,
            _hourly_units,
            _hourly,
        )
