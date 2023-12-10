from typing import Union


class OasisAndSandInstabilitySensor:
    def __init__(self, report_path: str):
        self.report_path = report_path
        self.sensors = []

        with open(self.report_path, "r", encoding="utf8") as f:
            for line in f:
                sensor = SensorReadings(line.strip())
                self.sensors.append(sensor)

    def extrapolate(self):
        return [s.get_next_value() for s in self.sensors]

    def extrapolate_backwards(self):
        return [s.get_previous_value() for s in self.sensors]


class SensorReadings:
    def __init__(self, readings: Union[str, list[int]]):
        self.readings = (
            list(map(int, readings.split(" ")))
            if isinstance(readings, str)
            else readings
        )

    def __repr__(self) -> str:
        return str(self.readings)

    def get_common_differences(self) -> list[int]:
        common_differences = []
        for i in range(len(self.readings) - 1):
            common_differences.append(self.readings[i + 1] - self.readings[i])

        assert len(common_differences) == len(self.readings) - 1, "Something is wrong"
        return common_differences

    def get_next_value(self) -> int:
        curr_cd = self.get_common_differences()
        sensors = [self]
        while any(map(lambda x: x != 0, curr_cd)):
            new_sensor = SensorReadings(curr_cd)
            curr_cd = new_sensor.get_common_differences()
            sensors.append(new_sensor)

        next_el = 0
        for sensor in reversed(sensors):
            next_el = sensor.readings[-1] + next_el
            sensor.readings.append(next_el)

        return self.readings[-1]

    def get_previous_value(self) -> int:
        curr_cd = self.get_common_differences()
        sensors = [self]
        while any(map(lambda x: x != 0, curr_cd)):
            new_sensor = SensorReadings(curr_cd)
            curr_cd = new_sensor.get_common_differences()
            sensors.append(new_sensor)

        prev_el = 0
        for sensor in reversed(sensors):
            prev_el = sensor.readings[0] - prev_el
            sensor.readings.insert(0, prev_el)

        return self.readings[0]
