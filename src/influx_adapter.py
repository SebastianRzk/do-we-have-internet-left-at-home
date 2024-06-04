from enum import Enum

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from config import Config
from history import History

WriteStatus = Enum('WriteStatus', ["OK", "FAILED"])


class InfluxWriter:
    def __init__(self, config: Config):
        self._bucket = config.influx_bucket
        self._org = config.influx_org
        self._token = config.influx_token
        # Store the URL of your InfluxDB instance
        self._write_api: influxdb_client.WriteApi | None = None
        self._url = config.influx_url

    def create_connection(self):
        client = influxdb_client.InfluxDBClient(
            url=self._url,
            token=self._token,
            org=self._org
        )
        # Write script
        self._write_api = client.write_api(write_options=SYNCHRONOUS)

    def write_point(self, point: influxdb_client.Point):
        self._write_api.write(bucket=self._bucket, org=self._org, record=point)

    def try_write_history(self, history: History) -> WriteStatus:
        try:
            self.create_connection()
            for history_event in history.events():
                point = influxdb_client.Point(measurement_name=history_event.event_category_name).time(
                    history_event.timestamp).field(
                    history_event.event_name, history_event.value
                )
                self.write_point(point)
            return WriteStatus.OK
        except:
            return WriteStatus.FAILED
