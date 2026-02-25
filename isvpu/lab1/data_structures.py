from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import NewType

Ppm = NewType("Ppm", int)
Lux = NewType("Lux", int)
Percent = NewType("Percent", float)
Temperature = NewType("Temperature", int)


@dataclass
class SystemConfig:
    temperature: Temperature
    humidity: Percent
    co2: Ppm
    luminosity: Lux
    people: bool
    time_of_day: Time


class Mode(Enum):
    OFF = "off"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Time(Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"


class Alert(Enum):
    SILENT = "silent"
    WARNING = "warning"
    ALARM = "alarm"
