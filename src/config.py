import env


class Config:
    def __init__(self, target_url: str,
                 timeout_in_seconds: int,
                 history_path: str,
                 influx_bucket: str,
                 influx_org: str,
                 influx_token: str,
                 influx_url: str):
        self.target_url = target_url
        self.timeout_in_seconds = timeout_in_seconds
        self.history_path = history_path
        self.influx_bucket = influx_bucket
        self.influx_org = influx_org
        self.influx_token = influx_token
        self.influx_url = influx_url


def get_config_from_env():
    return Config(
        target_url=env.get_from_env("TARGET_URL"),
        history_path=env.get_from_env_optional("HISTORY_FILE", "/history_data/history.json"),
        timeout_in_seconds=int(env.get_from_env_optional("TARGET_TIMEOUT", "5")),
        influx_bucket=env.get_from_env('INFLUX_BUCKET_NAME'),
        influx_org=env.get_from_env('INFLUX_ORG_NAME'),
        influx_token=env.get_from_env('INFLUX_AUTH_TOKEN'),
        influx_url=env.get_from_env('INFLUX_URL')
    )
