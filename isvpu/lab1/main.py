from controllers import (
    AlertControl,
    ClimateControl,
    FanControl,
    HumidityControl,
    LightMainControl,
    LightNightControl,
)
from data_structures import Lux, Percent, Ppm, SystemConfig, Temperature, Time
from main_controller import ControlSystem


def main():
    controller = ControlSystem(
        devices=[
            ClimateControl(),
            HumidityControl(),
            FanControl(),
            LightMainControl(),
            LightNightControl(),
            AlertControl(),
        ]
    )

    configs = [
        SystemConfig(
            temperature=Temperature(15),
            humidity=Percent(50),
            co2=Ppm(1900),
            luminosity=Lux(400),
            people=True,
            time_of_day=Time.EVENING,
        ),
        SystemConfig(
            temperature=Temperature(12),
            humidity=Percent(50),
            co2=Ppm(2100),
            luminosity=Lux(100),
            people=True,
            time_of_day=Time.EVENING,
        ),
        SystemConfig(
            temperature=Temperature(15),
            humidity=Percent(25),
            co2=Ppm(1900),
            luminosity=Lux(110),
            people=True,
            time_of_day=Time.EVENING,
        ),
    ]

    for i, config in enumerate(configs):
        controller.run(config)
        if i < len(configs) - 1:
            print("==" * 20 + "Новое состояние" + "==" * 20)


if __name__ == "__main__":
    main()
