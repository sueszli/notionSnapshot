import inspect
import logging
import functools
import argparse
import urllib.parse
import urllib.request
import os
import shutil
import glob
import hashlib
import mimetypes
import re
import sys
import uuid
from pathlib import Path
from typing import List, Tuple
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from bs4 import Tag
import html5lib  # used by bs4
import requests
import cssutils


class LoggingWrapper(logging.LoggerAdapter):
    # wrapper to automatically indent based on the call stack
    baseline = len(inspect.stack())

    @staticmethod
    def get_log():
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        return LoggingWrapper(logging.getLogger(), {})

    def process(self, msg, kwargs):
        indentation_level = len(inspect.stack()) - self.baseline - 4
        tab = " " * 3
        return f"{tab * indentation_level}{msg}", kwargs


LOG = LoggingWrapper.get_log()


def trace(print_args: bool = True):
    # decorator to log function calls and return values
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
            result = str(result) if result is not None else ""
            LOG.info(f"⬅ {result if print_args else ''}")
            return result

        return wrapper

    return decorator
