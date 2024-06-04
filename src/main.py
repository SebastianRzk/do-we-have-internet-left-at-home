import logging
import sys
from _datetime import datetime
from history import HistoryEvent, get_current_history, save_history
from config import get_config_from_env
from uptime import check_current_uptime_status

import influxdb_client

import influx_adapter

APPLICATION_EVENT_MEASUREMENT_NAME = "application_event"

CONTAINER_STARTED_EVENT_NAME = "container_started"
UPDATE_EVENT_STARTED = "checking_uptime"
SAVING_DATA_NAME  = "saving_data"
SAVING_DATA_NAME_VALUE_FAILED ="failed"
SAVING_DATA_NAME_VALUE_OK = "ok"

INITIAL_CHECK_PARAM = "--initial-check"

def create_container_started_event() -> HistoryEvent:
    return HistoryEvent(
        timestamp=datetime.now(),
        event_category_name=APPLICATION_EVENT_MEASUREMENT_NAME,
        event_name=APPLICATION_EVENT_MEASUREMENT_NAME,
        value=CONTAINER_STARTED_EVENT_NAME
    )


def create_uptime_check_event() -> HistoryEvent:
    return HistoryEvent(
        timestamp=datetime.now(),
        event_category_name=APPLICATION_EVENT_MEASUREMENT_NAME,
        event_name=APPLICATION_EVENT_MEASUREMENT_NAME,
        value=UPDATE_EVENT_STARTED
    )


def saving_data_failed_event() -> HistoryEvent:
    return HistoryEvent(
        timestamp=datetime.now(),
        event_category_name=APPLICATION_EVENT_MEASUREMENT_NAME,
        event_name=SAVING_DATA_NAME,
        value=SAVING_DATA_NAME_VALUE_FAILED
    )


def saving_data_ok_event() -> HistoryEvent:
    return HistoryEvent(
        timestamp=datetime.now(),
        event_category_name=APPLICATION_EVENT_MEASUREMENT_NAME,
        event_name=SAVING_DATA_NAME,
        value=SAVING_DATA_NAME_VALUE_OK
    )


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    config = get_config_from_env()

    history = get_current_history(config=config)

    if INITIAL_CHECK_PARAM in sys.argv:
        history.add_event(create_container_started_event())
    history.add_event(create_uptime_check_event())

    current_uptime_status = check_current_uptime_status(config=config)
    history.add_event(HistoryEvent.from_uptime_status(current_uptime_status))

    influxdb_adapter = influx_adapter.InfluxWriter(config=config)
    upload_status = influxdb_adapter.try_write_history(history=history)

    if upload_status == influx_adapter.WriteStatus.OK:
        history.prune_events()
        history.add_event(saving_data_ok_event())
    else:
        history.add_event(saving_data_failed_event())

    save_history(history=history, config=config)

    logging.info('finished')
