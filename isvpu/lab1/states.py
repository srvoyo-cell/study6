from dataclasses import dataclass

from data_structures import Alert, Mode


@dataclass
class ClimateControlStates:
    is_working: bool = False
    heating: Mode = Mode.OFF
    cooling: Mode = Mode.OFF
    rule: str | None = None


@dataclass
class HumidityControlStates:
    is_working: bool = False
    humidifying: Mode = Mode.OFF
    rule: str | None = None


@dataclass
class FanControlStates:
    is_working: bool = False
    speed: Mode = Mode.OFF
    rule: str | None = None


@dataclass
class LightMainStates:
    is_working: bool = False
    brightness: Mode = Mode.OFF
    flashing: bool = False
    rule: str | None = None


@dataclass
class LightNightStates:
    is_working: bool = False
    rule: str | None = None


@dataclass
class AlertStates:
    is_working: bool = False
    alert: Alert = Alert.SILENT
    rule: str | None = None
