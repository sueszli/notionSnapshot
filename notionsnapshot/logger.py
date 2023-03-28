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
    # proxy for 'logging' module that adds indentation based on the stack depth
    def process(self, msg, kwargs):
        tab = " " * 3
        ignored_stack_frames = 8
        indentation_level = len(traceback.extract_stack()) - ignored_stack_frames
        return f"{tab * indentation_level}{msg}", kwargs

    @staticmethod
    def get_log() -> logging.LoggerAdapter:
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        cssutils.log.setLevel(logging.CRITICAL)  # type: ignore

        os.system("cls" if os.name == "nt" else "clear")
        print(BANNER_ASCII)

        return LoggingWrapper(logging.getLogger("scrape-logger"), {})


LOG = LoggingWrapper.get_log()


def trace(print_args: bool = True):
    # decorator for @trace() to log functions arguments and return values
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            input_string = "⮕ "
            input_string += f"\033[92m{func.__name__}(\033[0m"
            if print_args:
                not_html = [arg for arg in args if not isinstance(arg, BeautifulSoup)]
                input_string += ", ".join([str(arg) for arg in not_html[1:]])
            input_string += f"\033[92m)\033[0m"
            LOG.info(input_string)

            result = func(*args, **kwargs)

            output_string = result if result is not None else ""
            LOG.info(f"⬅ {output_string if print_args else ''}")
            return result

        return wrapper

    return decorator
