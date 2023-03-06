import argparse
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.service import Service


class DriverInitializer:
    @staticmethod
    def get_driver(args: argparse.Namespace) -> webdriver.Chrome:
        # see flags here: https://github.com/GoogleChrome/chrome-launcher/blob/main/docs/chrome-flags-for-tools.md
        opts = Options()
        opts.add_argument("--disable-client-side-phishing-detection")
        opts.add_argument("--no-first-run")
        opts.add_argument("--enable-automation")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--silent")
        opts.add_argument("--disable-logging")
        opts.add_argument("--headless=new") if not args.show_browser else opts.add_argument("window-size=900,1200")
        opts.add_experimental_option("excludeSwitches", ["enable-logging"])
        os.environ["WDM_PROGRESS_BAR"] = str(0)
        os.environ["WDM_LOG"] = str(logging.NOTSET)

        chrome_executable: Service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=chrome_executable, options=opts)
        return driver
