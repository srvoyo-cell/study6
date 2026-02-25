from dataclasses import asdict
from enum import Enum
from typing import Any, Iterable, Protocol

from data_structures import SystemConfig


def _fmt(v: Any) -> str:
    if isinstance(v, Enum):
        return v.value
    if v is None:
        return "—"
    return str(v)


FIELD_NAMES = {
    "is_working": "Включен",
    "heating": "Нагрев",
    "cooling": "Охлаждение",
    "humidifying": "Увлажнение",
    "speed": "Скорость",
    "brightness": "Яркость",
    "alert": "Оповещение",
    "rule": "Правило",
    "flashing": "Мигание",
}


class Controller(Protocol):
    state: Any

    def compute(self, config: SystemConfig) -> None: ...
    def __str__(self) -> str: ...


class ControlSystem:
    def __init__(self, devices: Iterable[Controller]):
        self.devices = list(devices)
        self._prev_states: list[dict | None] = [None] * len(self.devices)

    def run(self, config: SystemConfig) -> None:
        for i, device in enumerate(self.devices):
            prev = self._prev_states[i]
            device.compute(config)
            curr = asdict(device.state)

            print(device)

            if prev is not None:
                changes = {k: (prev[k], curr[k]) for k in curr if prev[k] != curr[k]}
                if changes:
                    for field, (old, new) in changes.items():
                        label = FIELD_NAMES.get(field, field)
                        print(f"  ↳ {label}: {_fmt(old)} → {_fmt(new)}")

            self._prev_states[i] = curr
            print("-" * 40)
