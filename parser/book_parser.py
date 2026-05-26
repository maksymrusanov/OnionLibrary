import os
import time

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
    driver = webdriver.Firefox(options=options)
    driver.get(f"{os.getenv("LINK")}")
    return driver


def get_books(book_title):
    driver = get_web_driver()
    time.sleep(5)
    search_field = driver.find_element(By.NAME, "ask")
    search_field.click()
    search_field.send_keys(f"{book_title} ")
    search_field.submit()
    try:
        time.sleep(2)
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
    finally:
        driver.quit()


# finish downloading logic


def download_book(driver, book_url):
    driver = get_web_driver()
    try:
        driver.get(book_url)
        time.sleep(5)
        download_button = driver.find_element(
            By.XPATH, '//a[contains(@href, "/download/")]'
        )
        download_button.click()
        time.sleep(5)
    finally:
        driver.quit()
