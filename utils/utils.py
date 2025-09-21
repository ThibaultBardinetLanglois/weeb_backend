import os

def env_int(k):
    """
    Read an environment variable and return it as an integer.

    Ensures that numeric environment variables are interpreted
    as integers instead of strings.
    """
    return int(os.getenv(k))

def env_bool(k, default="False"):
    """
    Read an environment variable and return it as a boolean.

    Interprets common truthy values ("1", "true", "yes", "on")
    as True. All other values are considered False.
    """
    return str(os.getenv(k)).strip().lower() in {"1","true","yes","on"}