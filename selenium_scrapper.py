import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import uuid

import logging


class SeleniumScraper:
    def __init__(self):
        self.driver = None
        self.init_driver()

    def init_driver(self):
        logging.warning('Open WebDriver')
        user_agent = UserAgent().chrome
        options = Options()
        options.add_argument('--log-level=3')
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--incognito")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        # options.add_argument('--headless')
        options.add_argument(f'--user-agent={user_agent}')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="116.0.5845.96").install()),
                                       options=options)

    def click_element_by_class(self, class_name):
        wait = WebDriverWait(self.driver, 10)
        try:
            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
            element.click()
        except NoSuchElementException:
            print(f"Element with class '{class_name}' not found.")

    # def hover_over_element_by_class(self, class_name):
    #     wait = WebDriverWait(self.driver, 10)
    #     try:
    #         element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    #         actions = ActionChains(self.driver)
    #         actions.move_to_element(element).perform()
    #         # html = self.driver.find_element(By.ID, 'popup-root').get_attribute('innerHTML')
    #         # print(html)
    #     except NoSuchElementException:
    #         print(f"Element with class '{class_name}' not found.")

    def hover_over_element_by_class(self, class_name):
        wait = WebDriverWait(self.driver, 10)
        try:
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
            if element.is_displayed():
                time.sleep(1)
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
                time.sleep(5)
                # html = self.driver.find_element(By.ID, 'popup-root').get_attribute('innerHTML')
                # print(html)
            else:
                print(f"Element with class '{class_name}' is not visible.")
        except NoSuchElementException:
            print(f"Element with class '{class_name}' not found.")

    def click_element_by_xpath(self, xpath):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        time.sleep(2)
    # def hover_over_element_by_class(self, x, y):
    #     actions = ActionChains(self.driver)
    #     actions.move_by_offset(x, y).perform()
    def get_response(self, url):
        self.driver.get(url)
        page_source = self.driver.page_source
        return str(page_source)

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            logging.warning('Close WebDriver')
