import argparse
import urllib.parse
import urllib.request


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
        parser.add_argument("--debug", help="enable debugging", action="store_true")
        parser.add_argument("--no-cache", help="disable asset caching", action="store_true")
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
