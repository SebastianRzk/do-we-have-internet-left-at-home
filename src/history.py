import datetime
import json
import logging
import os
from typing import Self

from dateutil import parser

from config import Config
from status import UptimeStatus

HISTORY_FILE_TIMESTAMP_NAME = "timestamp"
HISTORY_FILE_IS_UP_NAME = "is_up"
HISTORY_FILE_EVENTS_NAME = "events"
HISTORY_FILE_EVENT_NAME = "event_name"
HISTORY_FILE_EVENT_CATEGORY_NAME = "event_category"
HISTORY_FILE_VALUE_NAME = "value"

HISTORY_EVENT_STATUS_CATEGORY_NAME = "uptime_status"
HISTORY_EVENT_UPTIME_STATUS_VALUE_UP = "up"
HISTORY_EVENT_UPTIME_STATUS_VALUE_DOWN = "down"


class HistoryEvent:
    def __init__(self, event_category_name: str, event_name: str, timestamp: datetime.datetime, value):
        self.event_category_name = event_category_name
        self.event_name = event_name
        self.timestamp = timestamp
        self.value = value

    @staticmethod
    def from_uptime_status(uptime_status: UptimeStatus):
        value = HISTORY_EVENT_UPTIME_STATUS_VALUE_UP
        if not uptime_status.is_up:
            value = HISTORY_EVENT_UPTIME_STATUS_VALUE_DOWN

        return HistoryEvent(
            event_name=HISTORY_EVENT_STATUS_CATEGORY_NAME,
            event_category_name=HISTORY_EVENT_STATUS_CATEGORY_NAME,
            timestamp=uptime_status.timestamp,
            value=value
        )

    @staticmethod
    def from_dict(content: dict) -> 'HistoryEvent':
        return HistoryEvent(
            event_category_name=content[HISTORY_FILE_EVENT_CATEGORY_NAME],
            event_name=content[HISTORY_FILE_EVENT_NAME],
            timestamp=parser.parse(content[HISTORY_FILE_TIMESTAMP_NAME]),
            value=content[HISTORY_FILE_VALUE_NAME]
        )

    def to_dict(self) -> dict:
        return {
            HISTORY_FILE_EVENT_CATEGORY_NAME: self.event_category_name,
            HISTORY_FILE_EVENT_NAME: self.event_name,
            HISTORY_FILE_TIMESTAMP_NAME: self.timestamp.isoformat(),
            HISTORY_FILE_VALUE_NAME: self.value
        }


class History:
    _events = []

    def with_events(self, events: list[HistoryEvent]) -> Self:
        self._events = events
        return self

    def to_dict(self) -> dict:
        return {
            HISTORY_FILE_EVENTS_NAME: [i.to_dict() for i in self._events],
        }

    @staticmethod
    def from_dict(history_file_content: dict) -> 'History':
        relevant_history = history_file_content[HISTORY_FILE_EVENTS_NAME]
        logging.info("history length: %s", len(relevant_history))
        if len(relevant_history) > 2*30*3+1:
            '''
            Prune after 2 hours
            '''
            logging.warning("Longer downtime, pruning list")
            logging.warning("history size before %s", len(relevant_history))
            first_part = relevant_history[0:1*30*3+1:1]
            last_part = relevant_history[-9::1]
            relevant_history = first_part + last_part
            logging.warning("history size after %s", len(relevant_history))
        return History().with_events(
            [HistoryEvent.from_dict(i) for i in relevant_history]
        )

    def add_event(self, event: HistoryEvent):
        self._events.append(event)

    def events(self) -> list[HistoryEvent]:
        return self._events

    def prune_events(self):
        self._events = []


def get_current_history(config: Config) -> History:
    if not os.path.isfile(config.history_path):
        logging.info("No history found in %s, contining", config.history_path)
        return History()
    history_file_content = json.load(open(config.history_path))
    return History.from_dict(history_file_content=history_file_content)


def save_history(history: History, config: Config) -> None:
    logging.info("Writing history to %s", config.history_path)
    with open(config.history_path, "w") as history_file:
        json.dump(history.to_dict(), history_file)
