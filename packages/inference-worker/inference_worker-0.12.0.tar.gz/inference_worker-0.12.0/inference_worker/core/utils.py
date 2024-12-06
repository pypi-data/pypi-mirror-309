import os

def get_env_variable(var_name):
    """Get the environment variable or raise a ValueError."""
    try:
        return os.environ[var_name]
    except KeyError:
        raise ValueError(f"The environment variable '{var_name}' is required but not set.")
