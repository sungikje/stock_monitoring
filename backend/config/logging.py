import logging
import os
import functools
from datetime import datetime, timedelta

from backend.config.env import BASE_DIR, LOG_PATH, PROJECT_NAME

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] - %(pathname)s, %(lineno)d : '%(message)s' "
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
log_file_name = datetime.today().strftime("%Y-%m-%d") + '.log'

today_log_path = os.path.join(BASE_DIR, LOG_PATH)
os.makedirs(today_log_path, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    filename=os.path.join(today_log_path, log_file_name),
    filemode="a",
)

logger = logging.getLogger(PROJECT_NAME)

def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        arg_list = [repr(a) for a in args]
        kwarg_list = [f"{k}={v!r}" for k, v in kwargs.items()]
        all_args = ", ".join(arg_list + kwarg_list)
        logger.info(f"CALL: {func.__name__}({all_args})")
        return func(*args, **kwargs)
    return wrapper