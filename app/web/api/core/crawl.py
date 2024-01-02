import hashlib
import multiprocessing
import re
from urllib.parse import urlparse

import scrapy
from bs4 import BeautifulSoup
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings

from app import OUTPUT_DIR


settings = get_project_settings()
settings.set("LOG_ENABLED", False)
settings.set("ROBOTSTXT_OBEY", False)


def get_last_url_segment(url):
    """Get the last segment of the URL, excluding query/fragment."""
    components = urlparse(url)
    path = components.path.rstrip("/")
    if not path:
        return "root"
    return path.split("/")[-1]


class MySpider(scrapy.Spider):
    name = "myspider"

    def __init__(self, start_url=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        parsed_url = urlparse(start_url)
        self.allowed_domains = [parsed_url.hostname]
        self.domain = parsed_url.netloc
        self.domain_path = OUTPUT_DIR / self.domain.replace(".", "_")
        self.domain_path.mkdir(parents=True, exist_ok=True)

    def parse(self, response):  # noqa
        self.log(f"Visited {response.url}")
        url_hash = hashlib.md5(response.url.encode("utf-8")).hexdigest()
        filename = f"{get_last_url_segment(response.url)}-{url_hash}.txt"
        page_path = self.domain_path / filename

        try:
            with page_path.open("w", encoding="utf-8") as file:
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text()
                cleaned_text = re.sub(r"\s+", " ", text).strip()
                file.write(cleaned_text)
        except IOError as e:
            self.log(f"Failed to write file {page_path}: {e}")

        for href in response.css("a::attr(href)").getall():
            url = response.urljoin(href)
            if urlparse(url).netloc == self.domain:
                yield scrapy.Request(url, callback=self.parse)


def run_spider(start_url):
    def spider_closed(spider, reason):
        create_master_file(start_url)

    dispatcher.connect(spider_closed, signal=signals.spider_closed)

    process = CrawlerProcess()
    process.crawl(MySpider, start_url=start_url)
    process.start()


def crawl_webpage(start_url):
    # Run Scrapy in a separate process
    crawler_process = multiprocessing.Process(target=run_spider, args=(start_url,))
    crawler_process.start()
    crawler_process.join()


def create_master_file(start_url: str):
    cleaned_url = urlparse(start_url).netloc.replace(".", "_")
    domain_path = OUTPUT_DIR / cleaned_url
    master_file_path = domain_path / f"{cleaned_url}_master_combined.txt"

    with master_file_path.open("w", encoding="utf-8") as master_file:
        for txt_file in domain_path.glob("*.txt"):
            try:
                master_file.write(txt_file.read_text(encoding="utf-8"))
            except IOError as e:
                print(f"Failed to read file {txt_file}: {e}")


if __name__ == "__main__":
    crawl_webpage("https://astelmach01.github.io/tinylang")
