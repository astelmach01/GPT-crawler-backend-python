import logging
import multiprocessing
import re
from datetime import datetime
from pathlib import Path
from typing import Set
from urllib.parse import urlparse
from urllib.parse import urlunparse

import scrapy
from bs4 import BeautifulSoup
from pydantic import HttpUrl
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings

from app import OUTPUT_DIR


settings = get_project_settings()
settings.set("ROBOTSTXT_OBEY", False)


def normalize_url(url):
    parsed_url = urlparse(url)
    normalized_path = re.sub(r"/{2,}", "/", parsed_url.path).rstrip("/")
    normalized_url = urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            normalized_path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )
    return normalized_url


class MySpider(scrapy.Spider):
    name = "my_spider"

    def __init__(self, start_url: str, depth_limit: int, *args, **kwargs) -> None:
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]

        self.visited_urls: Set = set()
        self.depth_limit = depth_limit

    def parse(self, response):  # noqa
        # Extract domain from start_url
        domain = urlparse(self.start_urls[0]).netloc
        domain_path = OUTPUT_DIR / domain.replace(".", "_")
        domain_path.mkdir(parents=True, exist_ok=True)

        for href in response.css("a::attr(href)").getall():
            absolute_url = response.urljoin(href)
            normalized_url = normalize_url(absolute_url)

            # Check if the URL belongs to the same domain and hasn't been visited
            if (
                urlparse(normalized_url).netloc == domain
                and normalized_url not in self.visited_urls
            ):
                self.visited_urls.add(normalized_url)
                self.log(
                    f"Visited URL: {normalized_url},"
                    f" total unique urls visited: {len(self.visited_urls)}"
                )

                if len(self.visited_urls) >= self.depth_limit:
                    raise CloseSpider(f"Reached depth limit of {self.depth_limit}")

                # Save page content to a file
                filename = (
                    f"{Path(normalized_url).name}"
                    f"-{datetime.now().strftime('%Y%m%d%H%M%S%f')}.txt"
                )
                file_path = OUTPUT_DIR / domain.replace(".", "_") / filename

                try:
                    with file_path.open("w", encoding="utf-8") as file:
                        soup = BeautifulSoup(response.text, "html.parser")
                        text = soup.get_text()
                        cleaned_text = re.sub(r"\s+", " ", text).strip()
                        file.write(cleaned_text)
                except IOError as e:
                    self.log(f"Failed to write file {file_path}: {e}")

                # Follow the link if it hasn't been visited and the depth limit
                # hasn't been reached
                yield scrapy.Request(normalized_url, callback=self.parse)


def run_spider(start_url: HttpUrl, depth_limit: int, *args, **kwargs):
    def spider_closed(spider, reason):
        create_master_file(start_url)

    dispatcher.connect(spider_closed, signal=signals.spider_closed)

    process = CrawlerProcess()

    process.crawl(
        MySpider, start_url=start_url, depth_limit=depth_limit, *args, **kwargs
    )
    process.start()


def crawl_webpage(start_url: str, depth_limit: int = 1000, *args, **kwargs):
    # Run Scrapy in a separate process
    crawler_process = multiprocessing.Process(
        target=run_spider, args=(start_url, depth_limit, *args), kwargs=kwargs
    )
    crawler_process.start()
    crawler_process.join()


def create_master_file(start_url: str):
    cleaned_url = urlparse(start_url).netloc.replace(".", "_")
    domain_path = OUTPUT_DIR / cleaned_url
    master_file_path = domain_path / f"{cleaned_url}_master_combined.txt"

    logging.info(f"Creating master file {master_file_path}")

    with master_file_path.open("w", encoding="utf-8") as master_file:
        for txt_file in domain_path.glob("*.txt"):
            try:
                master_file.write(txt_file.read_text(encoding="utf-8"))
            except IOError as e:
                print(f"Failed to read file {txt_file}: {e}")

    logging.info(f"Finished creating master file {master_file_path}")


if __name__ == "__main__":
    crawl_webpage("https://astelmach01.github.io/tinylang")
