import pandas as pd

"""
Don't even think about touching this, how it works is beyond even my understanding now. Leave it be and use it as shown 
in main.py
"""


class Event:
    def __init__(self):
        self.start = None
        self.end = None

    def add_start(self, start):
        self.start = start

    def add_end(self, end):
        self.end = end

    def clear(self):
        self.start = None
        self.end = None

    def to_dataframe(self):
        return pd.DataFrame(data={'Start': [self.start], 'End': [self.end]})

    def is_empty(self):
        return self.start is None and self.end is None

    def is_full(self):
        return not self.is_empty

    def is_only_start(self):
        return self.start is not None and self.end is None

    def is_only_end(self):
        return self.end is not None and self.start is None


class Point:
    def __init__(self, data):
        if isinstance(data, pd.Series):
            self.value = data[0]
            self.index = data.reset_index().iloc[0, 0]
        elif isinstance(data, list):
            self.value = data[0]
            self.index = data[1]

    def is_start(self, prev_value, threshold):
        return prev_value <= threshold < self.value

    def is_end(self, prev_value, threshold):
        return self.value <= threshold < prev_value

    def get_index(self):
        return self.index

    def get_value(self):
        return self.value


class EventDetector:
    def __init__(self, data):
        self.last_point = None
        self.series = data
        self.event_list = []
        self.threshold = 10
        self.final_event = Event()

    def detect_events(self, point_cache, event_cache=Event()):
        event = event_cache
        self.last_point = Point(point_cache)
        for index, value in self.series.items():
            point = Point([value, index])
            if point.is_start(self.last_point.value, self.threshold):
                if event.is_empty():
                    event.add_start(point.get_index())
                elif event.is_only_start():
                    self.event_list.append(event.to_dataframe())
                    event.add_start(point.get_index())

            if point.is_end(self.last_point.value, self.threshold):
                if event.is_only_start() or event.is_empty():
                    event.add_end(point.get_index())
                    self.event_list.append(event.to_dataframe())
                    event.clear()

            self.last_point = point

        if event.is_only_start():
            self.final_event = event

    def get_events(self):
        if not self.event_list:
            return None
        else:
            return pd.concat(self.event_list)

    def is_final_event_ongoing(self):
        return self.final_event.is_only_start()