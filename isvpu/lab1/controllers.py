from data_structures import (
    Alert,
    Lux,
    Mode,
    Percent,
    Ppm,
    SystemConfig,
    Temperature,
    Time,
)
from states import (
    AlertStates,
    ClimateControlStates,
    FanControlStates,
    HumidityControlStates,
    LightMainStates,
    LightNightStates,
)


class ClimateControl:
    def __init__(self):
        self.state = ClimateControlStates()

    def compute(self, config: SystemConfig):
        self.state = ClimateControlStates()
        t = config.temperature
        people = config.people
        time_of_day = config.time_of_day

        match (
            t < Temperature(18),
            t > Temperature(30),
            t > Temperature(26),
            people,
            time_of_day,
        ):
            case (True, _, _, _, Time.NIGHT):
                self.state.is_working = True
                self.state.heating = Mode.LOW
                self.state.rule = "R1"
            case (True, _, _, _, _):
                self.state.is_working = True
                self.state.heating = Mode.MEDIUM
                self.state.rule = "R2"
            case (_, True, _, _, _):
                self.state.is_working = True
                self.state.cooling = Mode.HIGH
                self.state.rule = "R3"
            case (False, False, True, True, _):  # явно: T <= 30 (не R3)
                self.state.is_working = True
                self.state.cooling = Mode.LOW
                self.state.rule = "R4"
            case _:
                self.state.rule = "R5"

    def __str__(self):
        return (
            "Состояние климат-контроля:\n"
            f"Включен: {'ДА' if self.state.is_working else 'НЕТ'}\n"
            f"Нагрев: {self.state.heating.value}\n"
            f"Охлаждение: {self.state.cooling.value}\n"
            f"ПРАВИЛО {self.state.rule}"
        )


class HumidityControl:
    def __init__(self):
        self.state = HumidityControlStates()

    def compute(self, config: SystemConfig):
        self.state = HumidityControlStates()
        humidity = config.humidity

        match (humidity < Percent(30), humidity < Percent(40)):
            case (True, _):
                self.state.is_working = True
                self.state.humidifying = Mode.HIGH
                self.state.rule = "R8"
            case (False, True):
                self.state.is_working = True
                self.state.humidifying = Mode.LOW
                self.state.rule = "R9"
            case _:
                self.state.rule = "R10"

    def __str__(self):
        return (
            "Состояние увлажнителя:\n"
            f"Включен: {'ДА' if self.state.is_working else 'НЕТ'}\n"
            f"Режим: {self.state.humidifying.value}\n"
            f"ПРАВИЛО {self.state.rule}"
        )


class FanControl:
    def __init__(self):
        self.state = FanControlStates()

    def compute(self, config: SystemConfig):
        self.state = FanControlStates()
        co2 = config.co2
        people = config.people

        match (co2 > Ppm(1500), co2 > Ppm(1000), people):
            case (True, _, _):
                self.state.is_working = True
                self.state.speed = Mode.HIGH
                self.state.rule = "R7"
            case (False, True, True):
                self.state.is_working = True
                self.state.speed = Mode.MEDIUM
                self.state.rule = "R6"
            case _:
                pass

    def __str__(self):
        return (
            "Состояние вентиляции:\n"
            f"Включен: {'ДА' if self.state.is_working else 'НЕТ'}\n"
            f"Скорость: {self.state.speed.value}\n"
            f"ПРАВИЛО {self.state.rule or '—'}"
        )


class LightMainControl:
    def __init__(self):
        self.state = LightMainStates()

    def compute(self, config: SystemConfig):
        self.state = LightMainStates()
        people = config.people
        time_of_day = config.time_of_day
        luminosity = config.luminosity
        temperature = config.temperature
        co2 = config.co2

        # R19: аварийный режим при тревоге (наивысший приоритет, игнорирует наличие людей)
        alarm = temperature > Temperature(35) or co2 > Ppm(2000)

        match (
            alarm,
            people,
            time_of_day,
            luminosity < Lux(100),
            luminosity < Lux(200),
            luminosity < Lux(400),
        ):
            case (True, _, _, _, _, _):  # R19: аварийный режим — мигание, max яркость
                self.state.is_working = True
                self.state.brightness = Mode.HIGH
                self.state.flashing = True
                self.state.rule = "R19"
            case (False, False, _, _, _, _):  # нет людей и нет аварии — выключено
                pass
            case (False, True, Time.NIGHT, True, _, _):  # R16
                self.state.is_working = True
                self.state.brightness = Mode.HIGH
                self.state.rule = "R16"
            case (False, True, _, _, True, _):  # R17
                self.state.is_working = True
                self.state.brightness = Mode.MEDIUM
                self.state.rule = "R17"
            case (False, True, _, _, _, True):  # R18
                self.state.is_working = True
                self.state.brightness = Mode.LOW
                self.state.rule = "R18"
            case _:
                pass

    def __str__(self):
        flashing_str = " (МИГАНИЕ)" if self.state.flashing else ""
        return (
            "Состояние основного освещения:\n"
            f"Включен: {'ДА' if self.state.is_working else 'НЕТ'}\n"
            f"Яркость: {self.state.brightness.value}{flashing_str}\n"
            f"ПРАВИЛО {self.state.rule or '—'}"
        )


class LightNightControl:
    def __init__(self):
        self.state = LightNightStates()

    def compute(self, config: SystemConfig):
        self.state = LightNightStates()
        luminosity = config.luminosity
        people = config.people
        time_of_day = config.time_of_day

        match (time_of_day, people, luminosity < Lux(50)):
            case (Time.NIGHT, True, True):
                self.state.is_working = True
                self.state.rule = "R11"
            case _:
                self.state.rule = "R12"

    def __str__(self):
        return (
            "Состояние ночной лампы:\n"
            f"Включен: {'ДА' if self.state.is_working else 'НЕТ'}\n"
            f"ПРАВИЛО {self.state.rule}"
        )


class AlertControl:
    def __init__(self):
        self.state = AlertStates()

    def compute(self, config: SystemConfig):
        self.state = AlertStates()
        temperature = config.temperature
        co2 = config.co2

        alarm = temperature > Temperature(35) or co2 > Ppm(2000)
        warning = temperature > Temperature(32) or co2 > Ppm(1800)

        match (alarm, warning):
            case (True, _):
                self.state.is_working = True
                self.state.alert = Alert.ALARM
                self.state.rule = "R13"
            case (False, True):
                self.state.is_working = True
                self.state.alert = Alert.WARNING
                self.state.rule = "R14"
            case _:
                self.state.rule = "R15"

    def __str__(self):
        return (
            "Состояние системы оповещения:\n"
            f"Включен: {'ДА' if self.state.is_working else 'НЕТ'}\n"
            f"Режим: {self.state.alert.value}\n"
            f"ПРАВИЛО {self.state.rule}"
        )
