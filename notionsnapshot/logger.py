import logging
import traceback
import functools
import os
from bs4 import BeautifulSoup
import cssutils


class LoggingWrapper(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        # proxy for logging module that adds indentation based on the stack depth
        ignored_stack_frames = 8
        indentation_level = len(traceback.extract_stack()) - ignored_stack_frames
        tab = " " * 3
        return f"{tab * indentation_level}{msg}", kwargs

    @staticmethod
    def get_log() -> logging.LoggerAdapter:
        LoggingWrapper._setup()
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        return LoggingWrapper(logging.getLogger(), {})

    @staticmethod
    def _setup() -> None:
        os.system("cls" if os.name == "nt" else "clear")
        cssutils.log.setLevel(logging.CRITICAL)  # type: ignore


LOG = LoggingWrapper.get_log()


def trace(print_args: bool = True):
    # for @trace decorator to log functions arguments and return values
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log_output = "⮕ "
            # before += f"{args[0].__class__.__name__}."
            log_output += f"\033[92m{func.__name__}(\033[0m"
            if print_args:
                not_html = [arg for arg in args if not isinstance(arg, BeautifulSoup)]
                log_output += ", ".join([str(arg) for arg in not_html[1:]])
            log_output += f"\033[92m)\033[0m"

            LOG.info(log_output)
            result = func(*args, **kwargs)
            if result is None:
                result = ""
            LOG.info(f"⬅ {result if print_args else ''}")
            return result

        return wrapper

    return decorator
