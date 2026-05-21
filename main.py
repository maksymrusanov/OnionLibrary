import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def get_web_driver():

    options = Options()

    options.set_preference("network.proxy.type", 1)
    options.set_preference("network.proxy.socks", "127.0.0.1")
    options.set_preference("network.proxy.socks_port", 9050)
    options.set_preference("network.proxy.socks_remote_dns", True)

    driver = webdriver.Firefox(options=options)
    driver.get(
        "http://flibustaongezhld6dibs2dps6vm4nvqg2kp7vgowbu76tzopgnhazqd.onion")
    return driver


def get_search_field(driver):

    search_field = driver.find_element(By.NAME, "ask")
    search_field.click()
    search_field.send_keys("Гарри Поттер")
    search_field.submit()
    print(search_field.text)
    return search_field


def close_web_driver(driver):
    driver.close()


def get_search_results(driver):
    search_results = driver.find_element(
        By.XPATH,
        "/html/body/div/div[2]/div[1]/div/ul[1]/li[1]/a",
    )
    search_results.click()


def get_books(driver):
    books = driver.find_elements(By.TAG_NAME, "a")
    for book in books:
        print(book.text)
    print(len(books))


if __name__ == "__main__":
    driver = get_web_driver()
    time.sleep(5)
    get_search_field(driver)
    time.sleep(5)
    get_search_results(driver)
    time.sleep(5)
    get_books(driver)
    time.sleep(1000)
    close_web_driver(driver)
