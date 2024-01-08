import hashlib
import logging
import os
from typing import Set
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def format_filename(url):
    parsed_url = urlparse(url)
    formatted_name = parsed_url.netloc + parsed_url.path
    return formatted_name.strip("/").replace("/", "_").replace("-", "_")


def fetch_page(driver, url, current_depth, max_depth, output_dir, visited):
    if url in visited or current_depth > max_depth:
        return
    visited.add(url)

    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    parsed_url = urlparse(url)
    file_name = format_filename(url) + "_text.txt"
    file_path = os.path.join(output_dir, file_name)

    # Extract text content from the body of the page
    text_content = driver.find_element(By.TAG_NAME, "body").get_attribute("innerText")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text_content)

    logging.info(
        f"Text content saved from {url} at depth {current_depth} to {file_path}"
    )

    # Collecting all links before visiting
    if current_depth < max_depth:
        hrefs = [
            link.get_attribute("href")
            for link in driver.find_elements(By.TAG_NAME, "a")
        ]
        for href in hrefs:
            if href and urlparse(href).netloc == parsed_url.netloc:
                fetch_page(
                    driver, href, current_depth + 1, max_depth, output_dir, visited
                )


def create_master_file(url, output_dir):
    formatted_name = format_filename(url)
    domain_path = os.path.join(output_dir, formatted_name)
    master_file_path = os.path.join(domain_path, f"{formatted_name}_master.txt")

    seen_hashes = set()

    with open(master_file_path, "w", encoding="utf-8") as master_file:
        for root, dirs, files in os.walk(domain_path):
            for file in files:
                if file.endswith("_text.txt"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line_hash = hashlib.md5(line.encode("utf-8")).hexdigest()
                            if line_hash not in seen_hashes:
                                master_file.write(line)
                                seen_hashes.add(line_hash)
                        master_file.write("\n\n")

    logging.info(f"Master file created at {master_file_path}")


async def crawl_webpage(url: str, max_depth: int = 100):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    domain_name = urlparse(url).netloc
    output_dir = os.path.join("output", domain_name)
    os.makedirs(output_dir, exist_ok=True)

    visited: Set = set()
    fetch_page(driver, url, 1, max_depth, output_dir, visited)

    driver.quit()

    create_master_file(url, "output")


async def main():
    URL = "https://nextjs.org"
    MAX_DEPTH = 2  # Adjust as needed
    await crawl_webpage(URL, MAX_DEPTH)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
