import logging

import traceback
import functools
from rich.logging import RichHandler
import os
from bs4 import BeautifulSoup
import cssutils

from argparser import ARGS


BANNER_ASCII = """
    _   __      __  _                _____                        __          __ 
   / | / /___  / /_(_)___  ____     / ___/____  ____ _____  _____/ /_  ____  / /_
  /  |/ / __ \\/ __/ / __ \\/ __ \\    \\__ \\/ __ \\/ __ `/ __ \\/ ___/ __ \\/ __ \\/ __/
 / /|  / /_/ / /_/ / /_/ / / / /   ___/ / / / / /_/ / /_/ (__  ) / / / /_/ / /_  
/_/ |_/\\____/\\__/_/\\____/_/ /_/   /____/_/ /_/\\__,_/ .___/____/_/ /_/\\____/\\__/  
                                                    /_/     
"""
HIGHLIGHTED_WORDS = []
IGNORED_STACK_FRAMES = 8


class LoggerWrapper(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        # add indentation based on stack depth
        tab_char = " " * 3
        indentation_level = len(traceback.extract_stack()) - IGNORED_STACK_FRAMES
        return f"{tab_char * indentation_level}{msg}", kwargs

    @staticmethod
    def configure_log() -> logging.LoggerAdapter:
        # see: https://rich.readthedocs.io/en/stable/reference/logging.html
        log_level = logging.DEBUG if ARGS.debug else logging.INFO
        rich_handler = RichHandler(rich_tracebacks=True, show_time=False, show_path=False, keywords=HIGHLIGHTED_WORDS)
        logging.basicConfig(level=log_level, format="%(message)s", handlers=[rich_handler])
        cssutils.log.setLevel(logging.CRITICAL)  # type: ignore
        return LoggerWrapper(logging.getLogger("scrape-logger"), {})


os.system("cls" if os.name == "nt" else "clear")
print(BANNER_ASCII)
LOG_SINGLETON = LoggerWrapper.configure_log()


def trace(print_args: bool = True):
    # decorator for @trace() to log functions arguments and return values
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            input_string = "⮕ "
            input_string += func.__name__ + "("
            if print_args:
                not_html = [arg for arg in args if not isinstance(arg, BeautifulSoup)]
                input_string += ", ".join([str(arg) for arg in not_html[1:]])
            input_string += ")"
            LOG_SINGLETON.info(input_string)

            result = func(*args, **kwargs)

            output_string = result if result is not None else ""
            LOG_SINGLETON.info(f"⬅ {output_string if print_args else ''}")
            return result

        return wrapper

    return decorator
