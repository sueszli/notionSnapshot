import urllib.parse
import urllib.request
import os
import shutil
import glob
import hashlib
import mimetypes
import re
import uuid
import time
from pathlib import Path
from typing import List, Optional, Tuple, Set

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from bs4 import BeautifulSoup, Tag
import html5lib  # implicitly used by bs4
import requests
import cssutils
from appdirs import user_cache_dir

from argparser import ARGS
from driver import DriverInitializer
from logger import LOG_SINGLETON as LOG, trace


class FileManager:
    output_dir: str = ""
    assets_dir: str = ""
    cache_dir: str = ""
    css_injection_file: str = ""
    js_injection_file: str = ""

    @staticmethod
    def setup() -> None:
        page_name = FileManager.get_page_name()
        FileManager.output_dir = os.path.join("snapshots", page_name)
        FileManager.assets_dir = os.path.join(FileManager.output_dir, "assets")

        cache_base_dir = user_cache_dir(appname="notion-snapshot", appauthor="sueszli")
        FileManager.cache_dir = os.path.join(cache_base_dir, page_name)

        FileManager._init_output_dir()

        css_file, js_file = FileManager._copy_injections_to_assets_dir()
        FileManager.css_injection_file = css_file
        FileManager.js_injection_file = js_file

    @staticmethod
    def get_page_name() -> str:
        page_id = urllib.parse.urlparse(ARGS.url).path[1:]
        return page_id[: page_id.rfind("-")].lower()

    @trace()
    @staticmethod
    def _init_output_dir() -> None:
        if not ARGS.disable_caching and os.path.exists(FileManager.assets_dir):
            shutil.copytree(FileManager.assets_dir, FileManager.cache_dir, dirs_exist_ok=True)
            LOG.info("cached assets from previous snapshot for this url")

        if os.path.exists(FileManager.output_dir):
            shutil.rmtree(FileManager.output_dir)
            LOG.info(f"removed previous snapshot for this url")

        os.makedirs(FileManager.output_dir, exist_ok=True)
        os.makedirs(FileManager.assets_dir, exist_ok=True)
        if not ARGS.disable_caching:
            os.makedirs(FileManager.cache_dir, exist_ok=True)

    @staticmethod
    def _copy_injections_to_assets_dir() -> Tuple[str, str]:
        injection_dir = Path(__file__).parent / "injections"
        css_out = Path(FileManager.assets_dir) / "injection.css"
        js_out = Path(FileManager.assets_dir) / "injection.js"
        shutil.copy(injection_dir / "injection.js", js_out)
        shutil.copy(injection_dir / "injection.css", css_out)
        relative_css_out = str(css_out.relative_to(FileManager.output_dir)).replace("\\", "/")
        relative_js_out = str(js_out.relative_to(FileManager.output_dir)).replace("\\", "/")
        return relative_css_out, relative_js_out

    @trace()
    @staticmethod
    def download_asset(url: str, filename: str = "") -> str:
        if not filename:
            filename = FileManager._generate_filename(url)

        already_downloaded = glob.glob(os.path.join(FileManager.assets_dir, filename + ".*"))
        if already_downloaded:
            LOG.info(f"asset '{filename}' was already downloaded")
            return str(Path(already_downloaded[0]).relative_to(FileManager.output_dir)).replace("\\", "/")

        if not ARGS.disable_caching and (cached := FileManager._load_from_cache(filename)) is not None:
            LOG.info(f"asset '{filename}' was found in cache")
            return cached

        destination = Path(FileManager.assets_dir) / filename
        try:
            session = requests.Session()
            session.trust_env = False
            response = session.get(url)
            response.raise_for_status()

            missing_file_extension = not bool(destination.suffix)
            if missing_file_extension:
                suffix = Path(urllib.parse.urlparse(url).path).suffix
                question_mark = "%3f"
                if suffix:
                    if question_mark in suffix.lower():
                        suffix = re.split(question_mark, suffix, flags=re.IGNORECASE)[0]
                    destination = destination.with_suffix(suffix)
                else:
                    content_type = response.headers.get("content-type")
                    assert content_type is not None
                    mimetype = mimetypes.guess_extension(content_type)
                    assert mimetype is not None
                    destination = destination.with_suffix(mimetype)

            with open(destination, "wb") as f:
                f.write(response.content)

            return str(destination.relative_to(FileManager.output_dir)).replace("\\", "/")

        except Exception as error:
            LOG.critical(f"error downloading asset on '{url}' - the online link to it will be used instead \n\t{error}")
            return str(Path(url)).replace("\\", "/")

    @staticmethod
    def _generate_filename(url: str) -> str:
        parsed_url = urllib.parse.urlparse(url)
        queryless_url = parsed_url.netloc + parsed_url.path
        params = urllib.parse.parse_qs(parsed_url.query)
        # having width in hash as name allows fetching different image resolutions
        if "width" in params.keys():
            queryless_url = queryless_url + f"?width={params['width']}"
        filename = hashlib.sha1(str.encode(queryless_url)).hexdigest()
        return filename

    @staticmethod
    def _load_from_cache(filename: str) -> Optional[str]:
        filename = filename if Path(filename).suffix else filename + ".*"
        cache_path = os.path.join(FileManager.cache_dir, filename)
        cached = glob.glob(cache_path)
        if cached:
            shutil.copy(cached[0], FileManager.assets_dir)
            return os.path.join("assets", os.path.basename(cached[0]))
        return None

    @staticmethod
    def save_page(soup: BeautifulSoup, url: str) -> None:
        # don't prettify html, it breaks the page
        html_str = str(soup)
        filename = FileManager.get_filename_from_url(url)
        output_path = Path(FileManager.output_dir + "/" + filename)
        with open(output_path, "wb") as f:
            f.write(html_str.encode("utf-8").strip())
        LOG.info(f"saved page\n\n\n\n\n\n\n")

    @staticmethod
    def get_filename_from_url(url: str) -> str:
        id = urllib.parse.urlparse(url).path[1:]
        filename = id[: id.rfind("-")].lower() + ".html"
        if url == ARGS.url:
            filename = "index.html"
        return filename


class Scraper:
    driver_download_path: str = os.path.abspath("snapshots/" + FileManager.get_page_name() + "/assets")
    driver: webdriver.Chrome = DriverInitializer.get_driver(driver_download_path)

    will_visit: Set[str] = set([ARGS.url])
    visited: Set[str] = set()

    @staticmethod
    def run() -> None:
        while Scraper.will_visit:
            url = Scraper.will_visit.pop()

            Scraper._load_page(url)
            Scraper._expand_toggle_blocks()
            soup = BeautifulSoup(Scraper.driver.page_source, "html5lib")
            Scraper._clean_up(soup)
            Scraper._download_images(soup)
            Scraper._download_stylesheets(soup)
            Scraper._download_pdfs(soup)
            Scraper._insert_injection_hooks(soup)
            Scraper._link_to_table_view_subpages(soup)
            subpage_urls = Scraper._link_anchors(soup)
            FileManager.save_page(soup, url)

            Scraper.visited.add(url)
            Scraper.will_visit.update(page for page in subpage_urls if page not in Scraper.visited)
            LOG.info(f"pages left to scrape: {len(Scraper.will_visit)}")

        Scraper.driver.quit()

    @trace()
    @staticmethod
    def _load_page(url: str) -> None:
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
                LOG.info(f"waiting for: {len(unknown_blocks)} unknown blocks - {len(loading_spinners)} loading spinners - {len(scrollers_with_children)}/{len(scrollers)} scrollers with children")
            prev_page = d.page_source
            return False

        Scraper.driver.get(url)
        try:
            WebDriverWait(Scraper.driver, ARGS.timeout).until(is_page_loaded)
        except TimeoutException:
            LOG.info("timed out waiting for page to load, proceeding anyways (might be because of infinite spinners)")
            time.sleep(10)
        LOG.info("page loaded")

        mode = "dark" if ARGS.dark_mode else "light"
        Scraper.driver.execute_script("__console.environment.ThemeStore.setState({ mode: '" + mode + "' })")
        LOG.info(f"set theme to {mode}-mode")

    @trace(print_args=False)
    @staticmethod
    def _expand_toggle_blocks(expanded_toggle_blocks=[]) -> None:
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
        assert all(isinstance(block, WebElement) for block in toggle_blocks), "toggle blocks should be web elements"

        for block in toggle_blocks:
            toggle_block_button = block.find_element(By.CSS_SELECTOR, "div[role=button]")
            block_style = toggle_block_button.find_element(By.TAG_NAME, "svg").get_attribute("style")
            assert isinstance(block_style, str), "toggle block style should be string"
            assert block_style is not None
            is_expanded = "(180deg)" in block_style
            if not is_expanded:
                Scraper.driver.execute_script("arguments[0].click();", toggle_block_button)
                try:
                    assert isinstance(block, WebElement), "toggle block should be web element"
                    WebDriverWait(Scraper.driver, ARGS.timeout).until(lambda d: is_block_expanded(block))
                except TimeoutException:
                    LOG.critical("timeout while expanding block - manually check if it's expanded in the snapshot")
                    continue
            expanded_toggle_blocks.append(block)

        nested_toggle_blocks = [block for block in get_toggle_blocks() if block not in expanded_toggle_blocks]
        LOG.info(f"expanded {len(expanded_toggle_blocks)} toggle blocks so far - found {len(nested_toggle_blocks)} nested blocks expand next")
        if nested_toggle_blocks:
            Scraper._expand_toggle_blocks(expanded_toggle_blocks)

    @staticmethod
    def _clean_up(soup: BeautifulSoup) -> None:
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

    @trace()
    @staticmethod
    def _download_images(soup: BeautifulSoup) -> None:
        images = [img for img in soup.findAll("img") if img.has_attr("src") and not (img.has_attr("class") and "notion-emoji" in img["class"])]
        LOG.info(f"found {len(images)} images to download")
        for img in images:
            is_notion_asset = img["src"].startswith("/")
            if "data:image" not in img["src"]:
                img_src = img["src"]
                if is_notion_asset:
                    img_src = f'https://www.notion.so{img["src"]}'
                img["src"] = FileManager.download_asset(img_src)
            elif is_notion_asset:
                img["src"] = f'https://www.notion.so{img["src"]}'

        emojis = [img for img in soup.findAll("img") if img.has_attr("class") and "notion-emoji" in img["class"]]
        LOG.info(f"found {len(emojis)} emojis to download")
        for img in emojis:
            style = cssutils.parseStyle(img["style"])
            spritesheet = style["background"]
            spritesheet_url = spritesheet[spritesheet.find("(") + 1 : spritesheet.find(")")]
            download_path = FileManager.download_asset(f"https://www.notion.so{spritesheet_url}")
            style["background"] = spritesheet.replace(spritesheet_url, download_path)
            img["style"] = style.cssText

        is_in_both = lambda img: img in images and img in emojis
        shared = [is_in_both(img) for img in images + emojis]
        assert not any(shared), "img is both an image and an emoji"

    @trace()
    @staticmethod
    def _download_stylesheets(soup: BeautifulSoup) -> None:
        def is_stylesheet(link):
            return link.has_attr("href") and link["href"].startswith("/") and "vendors~" not in link["href"]

        stylesheets = [link for link in soup.findAll("link", rel="stylesheet") if is_stylesheet(link)]
        base_url = "https://www.notion.so"

        for link in stylesheets:
            download_path = FileManager.download_asset(f'{base_url}{link["href"]}')

            css_file_path = os.path.join(FileManager.output_dir, download_path)
            # Open file with UTF-8 encoding
            with open(css_file_path, "r", encoding="utf-8") as f:
                css_content = f.read()

            # Write back with UTF-8 encoding
            with open(css_file_path, "w", encoding="utf-8") as f:
                url_pattern = re.compile(r"url\((https?:\/\/www\.notion\.so)?(\/[^)]+)\)")

                def url_replacer(match):
                    full_url, partial_url = match.groups()
                    if not full_url:
                        font_file_name = os.path.basename(partial_url)
                        font_download_url = f"{base_url}{partial_url}"
                        font_local_path = FileManager.download_asset(font_download_url, font_file_name)
                        return f"url({font_local_path})"
                    return match.group(0)

                # Replace the URLs in the CSS content
                modified_css_content = url_pattern.sub(url_replacer, css_content)
                f.write(modified_css_content)

            link["href"] = download_path

    @trace()
    @staticmethod
    def _download_pdfs(soup: BeautifulSoup) -> None:
        driver_blocks = Scraper.driver.find_elements(By.CLASS_NAME, "notion-file-block")
        driver_names = [[c.text for c in b.find_elements(By.XPATH, ".//*")][-2] for b in driver_blocks]
        assert len(driver_blocks) == len(driver_names), "number of driver blocks and names do not match"
        driver_pairs = [nb for nb in list(zip(driver_names, driver_blocks)) if nb[0].endswith(".pdf")]
        LOG.info(f"found {len(driver_pairs)} pdfs to download")

        # notion unpredictably adds spaces to names
        is_equal = lambda str1, str2: str1.replace(" ", "") == str2.replace(" ", "")
        is_in_list = lambda str1, str_list: any(is_equal(str1, str2) for str2 in str_list)

        for driver_name, driver_block in driver_pairs:
            download_name = driver_name.replace("/", "_").replace(":", "_")
            LOG.info(f"downloading file named '{download_name}'")

            if download_name in os.listdir(FileManager.assets_dir):
                LOG.info("pdf with same name was found in assets")

            elif not ARGS.disable_caching and FileManager._load_from_cache(download_name) is not None:
                LOG.info("pdf with same name was found in cache")

            else:
                assets_before_download = set(os.listdir(FileManager.assets_dir))

                try:
                    driver_block.click()
                except ElementClickInterceptedException:
                    webdriver.ActionChains(Scraper.driver).move_to_element(driver_block).click(driver_block).perform()
                    Scraper.driver.execute_script("arguments[0].click();", driver_block)
                    LOG.critical("clicking on pdf block was unsuccessful, consider running again with '-b' and clicking on it yourself")

                get_new_files = lambda: set(os.listdir(FileManager.assets_dir)) - assets_before_download
                is_downloaded = lambda: len(get_new_files()) == 1 and is_in_list(download_name, list(get_new_files()))
                while not is_downloaded():
                    time.sleep(0.25)
                    LOG.info(f"{get_new_files()} doesn't contain '{download_name}' yet")
                LOG.info(f"downloaded '{download_name}'")
                assert not re.compile(rf"{download_name} \(\d+\)\.pdf") in get_new_files(), "downloaded same pdf multiple times"

            soup_blocks = soup.findAll("div", {"class": "notion-file-block"})
            soup_names = [[c.text for c in b.find_all("div")][-2] for b in soup_blocks]
            assert len(soup_blocks) == len(soup_names), "number of soup blocks and names do not match"
            assert is_in_list(driver_name, soup_names), "driver name not found in soup names"

            soup_block = soup_blocks[soup_names.index(next(n for n in soup_names if is_equal(n, driver_name)))]
            soup_block.name = "a"
            soup_block["href"] = "./assets/" + download_name
            soup_block["style"] = "text-decoration: none; color: inherit;"
            soup_block["target"] = "_blank"

    @staticmethod
    def _insert_injection_hooks(soup: BeautifulSoup) -> None:
        # add ids and classes for 'injection.js' to work
        toggle_blocks = soup.findAll("div", {"class": "notion-toggle-block"})
        for query in ["header", "sub_header", "sub_sub_header"]:
            header_toggle_blocks = soup.findAll("div", {"class": f"notion-selectable notion-{query}-block"})
            [toggle_blocks.append(block) for block in header_toggle_blocks if block.select_one("div[role=button]") is not None]
        for toggle_block in toggle_blocks:
            toggle_button = toggle_block.select_one("div[role=button]")
            toggle_content = toggle_block.find("div", {"class": None, "style": ""})
            if toggle_button and toggle_content:
                toggle_button["class"] = toggle_block.get("class", []) + ["notionsnapshot-toggle-button"]
                toggle_content["class"] = toggle_content.get("class", []) + ["notionsnapshot-toggle-content"]
                toggle_content.attrs["notionsnapshot-toggle-id"] = toggle_button.attrs["notionsnapshot-toggle-id"] = uuid.uuid4()

        assert soup.head is not None
        soup.head.insert(-1, soup.new_tag("link", rel="stylesheet", href=FileManager.css_injection_file))
        assert soup.body is not None
        soup.body.insert(-1, soup.new_tag("script", type="text/javascript", src=FileManager.js_injection_file))

    @trace()
    @staticmethod
    def _link_to_table_view_subpages(soup: BeautifulSoup) -> None:
        # this function broke with a recent notion update
        tables = soup.findAll("div", {"class": "notion-table-view"})
        LOG.info(f"found {len(tables)} tables")
        for table in tables:
            rows = table.findAll("div", {"class": "notion-collection-item"})
            LOG.info(f"found {len(rows)} rows with links to subpages in table")
            for row in rows:
                subpage_path = "/" + row["data-block-id"].replace("-", "")
                row_name_span = row.find("span")
                # row_name_span["style"] = row_name_span["style"].replace("pointer-events: none;", "")
                subpage_anchor = soup.new_tag(
                    "a",
                    attrs={"href": subpage_path, "style": "cursor: pointer; color: inherit; text-decoration: none; fill: inherit;"},
                )
                row_name_span.wrap(subpage_anchor)

    @trace()
    @staticmethod
    def _link_anchors(soup: BeautifulSoup) -> List[str]:
        subpage_urls = []

        domain = f'{ARGS.url.split("notion.site")[0]}notion.site'
        anchors = soup.find_all("a", href=True)

        for a in anchors:
            url = a["href"]

            is_relative_url = url.startswith("/")
            if is_relative_url:
                url = f'{domain}/{a["href"].split("/")[-1]}'

            is_external_url = not url.startswith(domain)
            if is_external_url:
                continue

            scroller_parent = a.find_parent("div", class_="notion-scroller")
            is_scroller = scroller_parent is not None and len(scroller_parent) > 0
            topbar_parent = a.find_parent("div", class_="notion-topbar")
            is_topbar = topbar_parent is not None and len(topbar_parent) > 0
            is_table_of_contents = "#" in url

            if is_table_of_contents:
                # add ids and classes for 'injection.js' to work
                arr = url.split("#")
                url = arr[0]
                a["href"] = f"#{arr[-1]}"
                a["class"] = a.get("class", []) + ["notionsnapshot-anchor-link"]

            elif is_scroller or is_topbar:
                filename = FileManager.get_filename_from_url(url)
                a["href"] = filename
                subpage_urls.append(url)

            else:
                # remove all other links
                del a["href"]
                a.name = "span"
                children = [child for child in ([a] + a.find_all()) if child.has_attr("style")]
                for child in children:
                    style = cssutils.parseStyle(child["style"])
                    style["cursor"] = "default"
                    child["style"] = style.cssText

        return subpage_urls


if __name__ == "__main__":
    FileManager.setup()
    Scraper().run()
