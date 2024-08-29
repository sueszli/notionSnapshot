import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.service import Service

from argparser import ARGS


class DriverInitializer:
    @staticmethod
    def get_driver(file_download_path: str) -> webdriver.Chrome:
        # see: https://github.com/GoogleChrome/chrome-launcher/blob/main/docs/chrome-flags-for-tools.md
        opts = Options()
        opts.add_argument("--disable-client-side-phishing-detection")
        opts.add_argument("--no-first-run")
        opts.add_argument("--enable-automation")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--silent")
        opts.add_argument("--disable-logging")
        opts.add_argument("--headless=new") if not ARGS.show_browser else opts.add_argument("window-size=900,1200")
        opts.add_experimental_option("excludeSwitches", ["enable-logging"])

        # see: https://stackoverflow.com/questions/43470535/python-download-pdf-embedded-in-a-page/43471196#43471196
        profile = {
            "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
            "download.default_directory": file_download_path,
            "download.extensions_to_open": "",
            "plugins.always_open_pdf_externally": True,
        }
        opts.add_experimental_option("prefs", profile)

        os.environ["WDM_PROGRESS_BAR"] = str(0)
        os.environ["WDM_LOG"] = str(logging.NOTSET)

        executable_path = ChromeDriverManager().install()
        chrome_executable: Service = ChromeService(executable_path=executable_path)
        driver = webdriver.Chrome(service=chrome_executable, options=opts)
        return driver
