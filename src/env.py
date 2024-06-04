import os


def get_from_env(env_var_name: str) -> str:
    if env_var_name not in os.environ:
        raise Exception(f"Environment variable {env_var_name} has to be set!")
    return os.environ[env_var_name]


def get_from_env_optional(env_var_name: str, default: str) -> str:
    if env_var_name not in os.environ:
        return default
    return os.environ[env_var_name]