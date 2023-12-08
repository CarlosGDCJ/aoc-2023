class Race:
    def __init__(self, time: int, record: int):
        self.time = time
        self.record = record

    def distance_traveled(self, button_time):
        # This function has its max when button_time = time/2
        return button_time * (self.time - button_time)

    def button_times_to_beat_record(self):
        # max distance when button_time = time/2
        possible_button_times = list(range(self.time))
        # when time is odd, max is at time // 2 and time // 2 + 1
        is_odd = True if self.time % 2 != 0 else False
        left_side = possible_button_times[: len(possible_button_times) // 2 + is_odd]
        right_side = possible_button_times[len(possible_button_times) // 2 + is_odd :]

        def break_record(button_time):
            return self.distance_traveled(button_time) > self.record

        def doesnt_break_record(button_time):
            return self.distance_traveled(button_time) <= self.record

        # search for the first time that beats the record
        first_break = Race.find_threshold(left_side, condition=doesnt_break_record)
        # search for the last time that beats the record
        last_break = Race.find_threshold(right_side, condition=break_record)

        if first_break != -1 and last_break != -1:
            return possible_button_times[first_break : len(left_side) + last_break]
        elif first_break != -1:
            return possible_button_times[first_break]
        else:
            print("The record is unbeatable")

    @staticmethod
    def find_threshold(array: list[int], condition: callable) -> int:
        """Condition is True for the first N elements of array, then it becomes False. This function returns the index of the first False"""
        start = 0
        end = len(array)

        while start < end:
            distance = end - start
            mid = start + distance // 2

            if condition(array[mid]) == True:
                start = mid + 1
            else:
                end = mid

        if start > len(array):
            return -1

        return start
