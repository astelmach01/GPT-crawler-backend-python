import asyncio
import hashlib
import logging
from pathlib import Path
from typing import Set
from urllib.parse import urljoin
from urllib.parse import urlparse

from playwright.async_api import async_playwright


TIMEOUT = 60000  # page timeout in milliseconds, so 60 seconds
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
)


def should_follow_link(base_url, href) -> bool:
    if not href:
        return False

    # ignore anchor links
    if href.startswith("#"):
        return False

    parsed_base_url = urlparse(base_url)
    full_url = urljoin(base_url, href)
    parsed_full_url = urlparse(full_url)
    return (
        parsed_full_url.netloc == parsed_base_url.netloc
        and parsed_full_url.scheme in ["http", "https"]
    )


def format_filename(url):
    parsed_url = urlparse(url)
    formatted_name = parsed_url.netloc + parsed_url.path
    return formatted_name.strip("/").replace("/", "_").replace("-", "_")


async def fetch_page(browser, url, current_depth, max_depth, domain_dir, visited):
    if url in visited:
        logging.info(f"Skipping {url} (already visited)")
        return

    if current_depth > max_depth:
        logging.info(f"Skipping {url} (max depth reached)")
        return

    visited.add(url)

    logging.info(f"Fetching {url} at depth {current_depth}")
    page = await browser.new_page(user_agent=USER_AGENT)
    logging.info(f"Page created for {url}")

    try:
        await page.goto(url, timeout=TIMEOUT)
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        await page.close()
        return

    logging.info(f"Page loaded for {url}")

    await page.wait_for_selector("body")

    logging.info(f"Page body loaded for {url}")

    file_name = format_filename(url) + "_text.txt"
    file_path = domain_dir / file_name

    # Extract text content from the body of the page
    text_content = await page.inner_text("body")

    with file_path.open("w", encoding="utf-8") as file:
        file.write(text_content)

    logging.info(f"Saving {len(text_content)} characters to {file_path}")

    if current_depth < max_depth:
        href_elements = await page.query_selector_all("a")
        hrefs = [await href.get_attribute("href") for href in href_elements]

        logging.info(f"Found {len(hrefs)} links on {url}")

        for href in hrefs:
            if should_follow_link(url, href):
                full_url = urljoin(url, href)
                fetch_page(
                    browser,
                    full_url,
                    current_depth + 1,
                    max_depth,
                    domain_dir,
                    visited,
                )

    await page.close()


async def create_master_file(url, domain_dir):
    formatted_name = format_filename(url)
    master_file_path = domain_dir / f"{formatted_name}_master.txt"

    seen_hashes = set()

    with master_file_path.open("w", encoding="utf-8") as master_file:
        for file_path in domain_dir.glob("**/*_text.txt"):
            with file_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line_hash = hashlib.md5(line.encode("utf-8")).hexdigest()
                    if line_hash not in seen_hashes:
                        master_file.write(line)
                        seen_hashes.add(line_hash)
                master_file.write("\n\n")

    logging.info(f"Master file created at {master_file_path}")


async def crawl_webpage(url: str, max_depth: int = 2):
    async with async_playwright() as p:
        options = {"headless": True, "args": ["--no-sandbox"]}
        logging.info(f"Launching browser with options: {options} and timeout {TIMEOUT}")

        browser = await p.chromium.launch(**options)  # type: ignore

        domain_name = urlparse(url).netloc
        output_dir = Path("output")
        domain_dir = output_dir / domain_name
        domain_dir.mkdir(parents=True, exist_ok=True)

        visited: Set = set()
        await fetch_page(browser, url, 1, max_depth, domain_dir, visited)

        await browser.close()

        # if we didn't visit any pages, raise an exception
        if len(visited) == 0 or len(list(domain_dir.glob("**/*.txt"))) == 0:
            raise Exception(
                f"Could not crawl any pages at {url}, \
                            the page likely timed out"
            )

        await create_master_file(url, domain_dir)


async def main():
    URL = "https://nextjs.org"
    MAX_DEPTH = 2  # Adjust as needed
    logging.basicConfig(
        level=logging.INFO, format="%(message)s", handlers=[logging.StreamHandler()]
    )
    await crawl_webpage(URL, MAX_DEPTH)


if __name__ == "__main__":
    asyncio.run(main())
