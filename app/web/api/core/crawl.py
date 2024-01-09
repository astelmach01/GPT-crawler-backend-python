import asyncio
import hashlib
import logging
from pathlib import Path
from typing import Set
from urllib.parse import urljoin
from urllib.parse import urlparse

from playwright.async_api import async_playwright


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
    page = await browser.new_page()
    await page.goto(url)
    await page.wait_for_selector("body")

    file_name = format_filename(url) + "_text.txt"
    file_path = domain_dir / file_name

    # Extract text content from the body of the page
    text_content = await page.inner_text("body")

    with file_path.open("w", encoding="utf-8") as file:
        file.write(text_content)

    logging.info(f"Saving {len(text_content)} characters to {file_path}")

    # Collecting all links before visiting
    if current_depth < max_depth:
        href_elements = await page.query_selector_all("a")
        hrefs = [await href.get_attribute("href") for href in href_elements]

        logging.info(f"Found {len(hrefs)} links on {url}")

        for href in hrefs:
            if should_follow_link(url, href):
                await fetch_page(
                    browser,
                    urljoin(url, href),
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


async def crawl_webpage(url: str, max_depth: int = 100):
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        domain_name = urlparse(url).netloc
        output_dir = Path("output")
        domain_dir = output_dir / domain_name
        domain_dir.mkdir(parents=True, exist_ok=True)

        visited: Set = set()
        await fetch_page(browser, url, 1, max_depth, domain_dir, visited)

        await browser.close()

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
