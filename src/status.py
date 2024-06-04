from datetime import datetime


class UptimeStatus:
    def __init__(self, timestamp: datetime, is_up: bool):
        self.timestamp = timestamp
        self.is_up = is_up
