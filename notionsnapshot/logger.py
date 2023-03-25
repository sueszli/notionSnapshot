import logging
import traceback
import functools
import os
from bs4 import BeautifulSoup
import cssutils

BANNER_ASCII = """
    _   __      __  _                _____                        __          __ 
   / | / /___  / /_(_)___  ____     / ___/____  ____ _____  _____/ /_  ____  / /_
  /  |/ / __ \\/ __/ / __ \\/ __ \\    \\__ \\/ __ \\/ __ `/ __ \\/ ___/ __ \\/ __ \\/ __/
 / /|  / /_/ / /_/ / /_/ / / / /   ___/ / / / / /_/ / /_/ (__  ) / / / /_/ / /_  
/_/ |_/\\____/\\__/_/\\____/_/ /_/   /____/_/ /_/\\__,_/ .___/____/_/ /_/\\____/\\__/  
                                                    /_/     
"""


class LoggingWrapper(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        # proxy for 'logging' module that adds indentation based on the stack depth
        ignored_stack_frames = 8
        indentation_level = len(traceback.extract_stack()) - ignored_stack_frames
        tab = " " * 3
        return f"{tab * indentation_level}{msg}", kwargs

    @staticmethod
    def get_log() -> logging.LoggerAdapter:
        LoggingWrapper._setup()
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        return LoggingWrapper(logging.getLogger("scrape-logger"), {})

    @staticmethod
    def _setup() -> None:
        cssutils.log.setLevel(logging.CRITICAL)  # type: ignore
        os.system("cls" if os.name == "nt" else "clear")
        print(BANNER_ASCII)


LOG = LoggingWrapper.get_log()


def trace(print_args: bool = True):
    # decorator for @trace() to log functions arguments and return values
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log_input = "⮕ "
            # log_input += f"{args[0].__class__.__name__}."
            log_input += f"\033[92m{func.__name__}(\033[0m"
            if print_args:
                not_html = [arg for arg in args if not isinstance(arg, BeautifulSoup)]
                log_input += ", ".join([str(arg) for arg in not_html[1:]])
            log_input += f"\033[92m)\033[0m"
            LOG.info(log_input)

            result = func(*args, **kwargs)

            r = result if result is not None else ""
            LOG.info(f"⬅ {r if print_args else ''}")
            return result

        return wrapper

    return decorator
