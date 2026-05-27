import os
import time
import zipfile

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

load_dotenv()


def get_web_driver():
    options = Options()

    options.set_preference("network.proxy.type", 1)
    options.set_preference("network.proxy.socks", "127.0.0.1")
    options.set_preference("network.proxy.socks_port", 9050)
    options.set_preference("network.proxy.socks_remote_dns", True)

    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", os.path.abspath("books"))

    driver = webdriver.Firefox(options=options)

    url = os.getenv("LINK")
    if not url:
        raise ValueError("LINK environment variable not set")
    driver.get(url)

    return driver


driver = get_web_driver()


def get_books(book_title):
    search_field = driver.find_element(By.NAME, "ask")
    search_field.click()
    search_field.send_keys(f"{book_title} ")
    search_field.submit()
    try:
        time.sleep(5)
        items = driver.find_elements(By.XPATH, "//ul/li")
        res = []
        for li in items:
            try:
                title_el = li.find_element(
                    By.XPATH, './/a[contains(@href, "/b/")]')
                url = title_el.get_attribute("href")
            except NoSuchElementException:
                continue
            try:
                author_el = li.find_element(
                    By.XPATH, './/a[contains(@href, "/a/")]')
                author = author_el.text.strip()
            except NoSuchElementException:
                author = "not found"
            res.append(
                {
                    "title": title_el.text.strip(),
                    "author": author,
                    "url": url,
                }
            )
        return res
    except NoSuchElementException:
        print("No books found")
        return []


def download_book(book_url, file_form=None):
    create_folder("books")
    BOOK_FORMATS = {
        "epub",
        "fb2",
        "mobi",
        "pdf",
        "djvu",
        "txt",
        "rtf",
        "docx",
    }
    driver.get(book_url)

    links = driver.find_elements(By.XPATH, "//a[@href]")

    formats = {}

    for link in links:
        href = link.get_attribute("href")
        if not href:
            continue
        for fmt in BOOK_FORMATS:
            if f"/{fmt}" in href:
                formats[fmt] = href
    print("Available formats:", ", ".join(formats.keys()))
    if not formats:
        print("No formats found")
        return
    if file_form not in formats:
        file_form = (
            input("Enter format: " + ", ".join(formats.keys()) +
                  "\n> ").strip().lower()
        )
    if file_form not in formats:
        print("Invalid format selected")
        return
    driver.get(formats[file_form])
    print(f"Downloading in {file_form} format...")


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name


download_book(get_books("python")[3]["url"], "qwe")
# make it so files are downloaded into the books folder instead of the Downloads folder
# add unzip support for .zip format
# pass the extracted file
