import logging
import inspect
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
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.service import Service
import html5lib  # used by bs4
from bs4 import BeautifulSoup
from bs4 import Tag
import requests
import cssutils

cssutils.log.setLevel(logging.CRITICAL)  # type: ignore pylance type error
os.system("cls" if os.name == "nt" else "clear")


### LOGGING EXPERIMENTS ###
class LoggingWrapper(logging.LoggerAdapter):
    baseline = len(inspect.stack())

    def process(self, msg, kwargs):
        indentation_level = len(inspect.stack()) - self.baseline - 3
        return f"{'+' * indentation_level}{msg}", kwargs


logger = LoggingWrapper(logging.getLogger(__name__), {})
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def f3():
    logger.info("I am f3")


def f2():
    logger.info("I am f2")
    f3()


def f1():
    logger.info("I am f1")
    f2()


def go():
    logger.info("I am go.")
    f1()
    f2()
    f3()


f1()
go()


def trace_decorator(func):
    def wrapper(*args, **kwargs):
        entry_content = ""
        if len(args) > 1:
            entry_content += f"{args[0].__class__.__name__}."
        entry_content += f"{func.__name__}({', '.join([str(arg) for arg in args[1:]])})"
        logger.info(entry_content)
        return func(*args, **kwargs)

    return wrapper


### LOGGING EXPERIMENTS ###


class ArgParser:
    @staticmethod
    def get_arguments() -> argparse.Namespace:
        args = ArgParser._parse_arguments()
        ArgParser._validate_url(args.url)
        ArgParser._validate_timeout(args.timeout)
        return args

    @staticmethod
    def _parse_arguments() -> argparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument("-b", "--show-browser", help="disable headless mode and show browser window", action="store_true")
        parser.add_argument("-d", "--dark-mode", help="scrape pages in dark mode", action="store_true")
        parser.add_argument("--timeout", help="specify download timeout in seconds (default: 10s)", type=int, default=10, metavar="TIMEOUT")
        parser.add_argument("url", help="url of the Notion page to scrape", metavar="URL")
        parser.parse_args()
        return parser.parse_args()

    @staticmethod
    def _validate_timeout(timeout: int) -> None:
        if timeout < 0:
            raise argparse.ArgumentTypeError("timeout not positive")

    @staticmethod
    def _validate_url(url_str: str) -> None:
        url = urllib.parse.urlparse(url_str)
        if url.scheme != "https":
            raise argparse.ArgumentTypeError("url doesn't start with https://")
        if not url.netloc.endswith(".notion.site"):
            raise argparse.ArgumentTypeError("url is missing 'notion.site' domain")
        if not url.path.startswith("/"):
            raise argparse.ArgumentTypeError("url doesn't contain an id")
        if url.fragment:
            raise argparse.ArgumentTypeError("url contains a fragment ('#')")


class DriverInitializer:
    @staticmethod
    def get_driver(args: argparse.Namespace) -> webdriver.Chrome:
        print(f"DriverInitializer.get_driver()")
        # chose Selenium instead of Playwright for simpler installation with the webdriver_manager package
        # see flags: https://github.com/GoogleChrome/chrome-launcher/blob/main/docs/chrome-flags-for-tools.md
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


class FileManager:
    output_dir = ""

    def __init__(self, args: argparse.Namespace) -> None:
        print(f"FileManager.__init__()")
        id = urllib.parse.urlparse(args.url).path[1:]
        name = id[: id.rfind("-")].lower()
        FileManager.output_dir = os.path.join("snapshots", name)

        if os.path.exists(FileManager.output_dir):
            shutil.rmtree(FileManager.output_dir)
            print(f"\tremoved previous snapshot for this url")

        os.makedirs(FileManager.output_dir, exist_ok=True)
        os.makedirs(FileManager.output_dir + "/assets", exist_ok=True)

    def download_asset(self, url: str, filename: str = "") -> Path:
        if not filename:
            parsed_url = urllib.parse.urlparse(url)
            queryless_url = parsed_url.netloc + parsed_url.path
            params = urllib.parse.parse_qs(parsed_url.query)
            # having width in hash as name allows fetching different image resolutions
            if "width" in params.keys():
                queryless_url = queryless_url + f"?width={params['width']}"
            filename = hashlib.sha1(str.encode(queryless_url)).hexdigest()
        print(f"\tFileManager.download_asset({filename})")

        matching_file = glob.glob(FileManager.output_dir + "/assets/" + filename + ".*")
        if matching_file:
            return Path(matching_file[0]).relative_to(FileManager.output_dir)

        destination = Path(FileManager.output_dir) / "assets" / filename
        try:
            session = requests.Session()
            session.trust_env = False
            response = session.get(url)
            response.raise_for_status()

            has_file_extension = bool(destination.suffix)
            if not has_file_extension:
                suffix = Path(urllib.parse.urlparse(url).path).suffix
                if suffix:
                    if "%3f" in suffix.lower():
                        suffix = re.split("%3f", suffix, flags=re.IGNORECASE)[0]
                    destination = destination.with_suffix(suffix)
                else:
                    content_type = response.headers.get("content-type")
                    assert content_type is not None
                    mimetype = mimetypes.guess_extension(content_type)
                    assert mimetype is not None
                    destination = destination.with_suffix(mimetype)

            with open(destination, "wb") as f:
                f.write(response.content)
            return destination.relative_to(FileManager.output_dir)

        except Exception as error:
            print(f"error downloading asset on '{url}' - a hyperlink will be used in snapshot instead", file=sys.stderr)
            print(error, file=sys.stderr)
            return Path(url)

    def copy_injections_to_assets(self) -> Tuple[str, str]:
        print("\tFileManager.copy_injections_to_assets()")
        injection_dir = Path(__file__).parent / "injections"
        css_out = Path(FileManager.output_dir) / "assets" / "injection.css"
        js_out = Path(FileManager.output_dir) / "assets" / "injection.js"
        print(f"CSS_OUT: {css_out}  JS_OUT: {js_out}")
        shutil.copy(injection_dir / "injection.js", js_out)
        shutil.copy(injection_dir / "injection.css", css_out)

        # Path Fix
        relative_css_out = str(css_out.relative_to(FileManager.output_dir)).replace("\\","/")
        relative_js_out = str(js_out.relative_to(FileManager.output_dir)).replace("\\","/")

       # print(f"RELATIVE CSS: {relative_css_out}")
       # print(f"RELATIVE JS: {relative_js_out}")

        return relative_css_out,relative_js_out

    def save_page(self, soup: BeautifulSoup, url: str) -> None:
        print(f"\tFileManager.save_page({url})")
        soup.prettify()
        html_str = str(soup)
        output_path = self.get_path_from_url(url)
        with open(output_path, "wb") as f:
            f.write(html_str.encode("utf-8").strip())

    def get_path_from_url(self, url: str) -> Path:
        print(f"\tFileManager.get_path_from_url({url})")
        id = urllib.parse.urlparse(url).path[1:]
        filename = id[: id.rfind("-")].lower() + ".html"
        if url == Scraper.args.url:
            filename = "index.html"
        return Path(FileManager.output_dir + "/" + filename)


class Scraper:
    args = ArgParser.get_arguments()
    driver = DriverInitializer.get_driver(args)
    file_manager = FileManager(args)

    will_visit = set([args.url])
    visited = set()

    def run(self) -> None:
        print(f"Scraper.run()")
        while Scraper.will_visit:
            #self._pages_to_visit(Scraper.will_visit)
            url = Scraper.will_visit.pop()

            self._load_page(url)
            self._expand_toggle_blocks()
            soup = BeautifulSoup(Scraper.driver.page_source, "html5lib")
            self._clean_up(soup)
            self._download_images(soup)
            self._download_stylesheets(soup)
            self._insert_injections(soup)
            self._link_to_table_view_subpages(soup)
            subpage_urls = self._link_to_subpages(soup)

            Scraper.file_manager.save_page(soup, url)
            Scraper.visited.add(url)

            [Scraper.will_visit.add(page) for page in subpage_urls if page not in Scraper.visited]
            #self._pages_to_visit(Scraper.will_visit)

    
    def _pages_to_visit(self,pages:set | list):
        print("Pages currently to be looked at: ")
        for page in pages: 
            print(page)
    

                
    def _load_page(self, url: str) -> None:
        print(f"Scraper._load_page({url})")
        prev_page = ""

        def is_page_loaded(d: webdriver.Chrome) -> bool:
            nonlocal prev_page
            root_block = d.find_elements(By.CLASS_NAME, "notion-presence-container")
            if root_block:
                unknown_blocks = d.find_elements(By.CLASS_NAME, "notion-unknown-block")
                loading_spinners = d.find_elements(By.CLASS_NAME, "loading-spinner")
                scrollers = d.find_elements(By.CLASS_NAME, "notion-scroller")
                scrollers_with_children = [scroller for scroller in scrollers if scroller.find_elements(By.TAG_NAME, "div")]
                page_changed = prev_page != d.page_source
                all_scrollers_loaded = len(scrollers_with_children) == len(scrollers)
                if all_scrollers_loaded and not unknown_blocks and not loading_spinners and not page_changed:
                    return True
                print(f"\twaiting for: {len(unknown_blocks)} unknown blocks - {len(loading_spinners)} loading spinners - {len(scrollers_with_children)}/{len(scrollers)} scrollers with children")
            prev_page = d.page_source
            return False

        Scraper.driver.get(url)
        WebDriverWait(Scraper.driver, Scraper.args.timeout).until(is_page_loaded)

        mode = "dark" if Scraper.args.dark_mode else "light"
        Scraper.driver.execute_script("__console.environment.ThemeStore.setState({ mode: '" + mode + "' })")

    def _expand_toggle_blocks(self, expanded_toggle_blocks=[]) -> None:
        print(f"Scraper._expand_toggle_blocks() - {len(expanded_toggle_blocks)} expanded so far")

        def get_toggle_blocks() -> List[WebElement]:
            toggle_blocks = Scraper.driver.find_elements(By.CLASS_NAME, "notion-toggle-block")
            header_toggle_blocks = []
            queries = [f"notion-selectable.notion-{type}-block" for type in ["header", "sub_header", "sub_sub_header"]]
            for query in queries:
                blocks = Scraper.driver.find_elements(By.CLASS_NAME, query)
                for block in blocks:
                    if block.find_elements(By.CSS_SELECTOR, "div[role=button]"):
                        header_toggle_blocks.append(block)
            toggle_blocks += header_toggle_blocks
            return toggle_blocks

        def is_block_expanded(b: WebElement) -> bool:
            content = b.find_element(By.CSS_SELECTOR, "div:not([style]")
            unknown_children = b.find_elements(By.CLASS_NAME, "notion-unknown-block")
            is_loading = b.find_elements(By.CLASS_NAME, "loading-spinner")
            return content and not unknown_children and not is_loading

        toggle_blocks = get_toggle_blocks()
        toggle_blocks = [block for block in toggle_blocks if block not in expanded_toggle_blocks]

        for block in toggle_blocks:
            toggle_block_button = block.find_element(By.CSS_SELECTOR, "div[role=button]")
            is_expanded = "(180deg)" in (toggle_block_button.find_element(By.TAG_NAME, "svg").get_attribute("style"))
            if not is_expanded:
                Scraper.driver.execute_script("arguments[0].click();", toggle_block_button)
                try:
                    WebDriverWait(Scraper.driver, Scraper.args.timeout).until(lambda d: is_block_expanded(block))
                except TimeoutException:
                    print("timeout while expanding block - manually check if it's expanded in the snapshot", file=sys.stderr)
                    continue
            expanded_toggle_blocks.append(block)

        nested_toggle_blocks = [block for block in get_toggle_blocks() if block not in expanded_toggle_blocks]
        print(f"\texpanded {len(toggle_blocks)} toggleable blocks, found {len(nested_toggle_blocks)} children to expand next")
        if nested_toggle_blocks:
            self._expand_toggle_blocks(expanded_toggle_blocks)

    def _clean_up(self, soup: BeautifulSoup) -> None:
        print("Scraper._clean_up()")
        for script in soup.findAll("script"):
            script.decompose()
        for aif_production in soup.findAll("iframe", {"src": "https://aif.notion.so/aif-production.soup"}):
            aif_production.decompose()
        for intercom_frame in soup.findAll("iframe", {"id": "intercom-frame"}):
            intercom_frame.decompose()
        for intercom_div in soup.findAll("div", {"class": "intercom-lightweight-app"}):
            intercom_div.decompose()
        for overlay_div in soup.findAll("div", {"class": "notion-overlay-container"}):
            overlay_div.decompose()
        for vendors_css in soup.find_all("link", href=lambda text: bool(text) and "vendors~" in text):
            vendors_css.decompose()
        for collection_selector in soup.findAll("div", {"class": "notion-collection-view-select"}):
            collection_selector.decompose()
        for tag in ["description", "twitter:card", "twitter:site", "twitter:title", "twitter:description", "twitter:image", "twitter:url", "apple-itunes-app"]:
            unwanted_tag = soup.find("meta", attrs={"name": tag})
            if unwanted_tag and isinstance(unwanted_tag, Tag):
                unwanted_tag.decompose()
        for tag in ["og:site_name", "og:type", "og:url", "og:title", "og:description", "og:image"]:
            unwanted_og_tag = soup.find("meta", attrs={"property": tag})
            if unwanted_og_tag and isinstance(unwanted_og_tag, Tag):
                unwanted_og_tag.decompose()

    def _download_images(self, soup: BeautifulSoup) -> None:
        print("Scraper._download_images()")
        images = [img for img in soup.findAll("img") if img.has_attr("src")]
        for img in images:
            is_notion_asset = img["src"].startswith("/")
            if "data:image" not in img["src"]:
                img_src = img["src"]
                if is_notion_asset:
                    img_src = f'https://www.notion.so{img["src"]}'
                src_link = Scraper.file_manager.download_asset(img_src)

                # Path fix
                img["src"] = str(src_link).replace("\\","/")
            elif is_notion_asset:
                img["src"] = f'https://www.notion.so{img["src"]}'

        emojis = [img for img in soup.findAll("img") if img.has_attr("class") and "notion-emoji" in img["class"]]
        for img in emojis:
            style = cssutils.parseStyle(img["style"])
            spritesheet = style["background"]
            spritesheet_url = spritesheet[spritesheet.find("(") + 1 : spritesheet.find(")")]
            download_path = Scraper.file_manager.download_asset(f"https://www.notion.so{spritesheet_url}")
            
            # Path fix
            download_path = str(download_path).replace("\\","/")
            
            style["background"] = spritesheet.replace(spritesheet_url, download_path)
            img["style"] = style.cssText

    def _download_stylesheets(self, soup: BeautifulSoup) -> None:
        print("Scraper._download_stylesheets()")
        is_stylesheet = lambda link: link.has_attr("href") and link["href"].startswith("/") and not "vendors~" in link["href"]
        stylesheets = [link for link in soup.findAll("link", rel="stylesheet") if is_stylesheet(link)]
        for link in stylesheets:
            download_path = Scraper.file_manager.download_asset(f'https://www.notion.so{link["href"]}')
            with open(FileManager.output_dir / download_path, "rb+") as f:
                stylesheet = cssutils.parseString(f.read())
                for rule in stylesheet.cssRules:
                    if rule.type == cssutils.css.CSSRule.FONT_FACE_RULE:
                        font_file = rule.style["src"].split("url(")[-1].split(")")[0]
                        parent_css_path = os.path.split(urllib.parse.urlparse(link["href"]).path)[0]
                        font_url = "/".join(p.strip("/") for p in ["https://www.notion.so", parent_css_path, font_file] if p.strip("/"))
                        download_path2 = Scraper.file_manager.download_asset(font_url, Path(font_file).name)

                        # Path Fix
                        download_path2 = str(download_path2).replace("\\","/")
                        rule.style["src"] = f"url({download_path2})"
                f.seek(0)
                f.truncate()
                f.write(stylesheet.cssText)
                # Path Fix
                download_path = str(download_path).replace("\\","/")
            
            link["href"] = download_path

    def _insert_injections(self, soup: BeautifulSoup) -> None:
        print("Scraper._insert_injections()")
        # add ids and classes to toggle blocks for the injections, inserted next
        toggle_blocks = soup.findAll("div", {"class": "notion-toggle-block"})
        for query in ["header", "sub_header", "sub_sub_header"]:
            header_toggle_blocks = soup.findAll("div", {"class": f"notion-selectable notion-{query}-block"})
            [toggle_blocks.append(block) for block in header_toggle_blocks if block.select_one("div[role=button]") is not None]
        for toggle_block in toggle_blocks:
            toggle_id = uuid.uuid4()
            toggle_button = toggle_block.select_one("div[role=button]")
            toggle_content = toggle_block.find("div", {"class": None, "style": ""})
            if toggle_button and toggle_content:
                toggle_button["class"] = toggle_block.get("class", []) + ["notionsnapshot-toggle-button"]
                toggle_content["class"] = toggle_content.get("class", []) + ["notionsnapshot-toggle-content"]
                toggle_content.attrs["notionsnapshot-toggle-id"] = toggle_button.attrs["notionsnapshot-toggle-id"] = toggle_id

        css_path, js_path = Scraper.file_manager.copy_injections_to_assets()



        assert soup.head is not None
        soup.head.insert(-1, soup.new_tag("link", rel="stylesheet", href=str(css_path)))
        assert soup.body is not None
        soup.body.insert(-1, soup.new_tag("script", type="text/javascript", src=str(js_path)))

    def _link_to_table_view_subpages(self, soup: BeautifulSoup) -> None:
        print("Scraper._link_to_table_view_subpages()")
        # add links to the title rows (which are identical to the data-block-id without dashes)
        for table_view in soup.findAll("div", {"class": "notion-table-view"}):
            for table_row in table_view.findAll("div", {"class": "notion-collection-item"}):
                table_row_block_id = table_row["data-block-id"]
                table_row_href = "/" + table_row_block_id.replace("-", "")
                row_target_span = table_row.find("span")
                row_target_span["style"] = row_target_span["style"].replace("pointer-events: none;", "")
                row_link_wrapper = soup.new_tag(
                    "a",
                    attrs={"href": table_row_href, "style": "cursor: pointer; color: inherit; text-decoration: none; fill: inherit;"},
                )
                row_target_span.wrap(row_link_wrapper)

    def _link_to_subpages(self, soup: BeautifulSoup) -> List[str]:
        print("Scraper._link_to_subpages()")
        subpage_urls = []
        domain = f'{Scraper.args.url.split("notion.site")[0]}notion.site'
        #print(domain)
        # Locate all links ("a" elements) in the document
        for a in soup.find_all("a", href=True):
            url = a["href"]
            if url.startswith("/"):
                # if url is a relative path, add the domain to the beginning
                url = f'{domain}/{a["href"].split("/")[len(a["href"].split("/"))-1]}'
            if not url.startswith(domain):
                # if the url isnt the domain (notion.page) we don't want it 
                continue

            #print(f"URL OF PAGE: {url}")

            is_scroller = len(a.find_parents("div", class_="notion-scroller")) > 0
            if is_scroller:
                #print("ITS A SCROLLER")
                del a["href"]
                a.name = "span"
                children = [child for child in ([a] + a.find_all()) if child.has_attr("style")]
                for child in children:
                    style = cssutils.parseStyle(child["style"])
                    style["cursor"] = "default"
                    child["style"] = style.cssText
            else:
                #print("ITS NOT A SCROLLER")
                if "#" in url:
                    arr = url.split("#")
                    url = arr[0]
                    a["href"] = f"#{arr[-1]}"
                    a["class"] = a.get("class", []) + ["notionsnapshot-anchor-link"]
                else:
                    a["href"] = Scraper.file_manager.get_path_from_url(url)
                #print(f"THIS IS A URL: {url}")    
                subpage_urls.append(url)
        return subpage_urls

    def __del__(self):
        Scraper.driver.quit()
        print("closed browser")


if __name__ == "__main__":
    # Scraper().run()
    pass
