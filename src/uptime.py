import requests
from status import UptimeStatus
from datetime import datetime
from config import Config


def check_current_uptime_status(config: Config) -> UptimeStatus:
    now = datetime.now()
    try:
        result = requests.head(url=config.target_url, timeout=config.timeout_in_seconds)
        is_up = result.status_code and result.status_code < 210
        return UptimeStatus(timestamp=now, is_up=is_up)
    except:
        return UptimeStatus(timestamp=now, is_up=False)
