# import time
#
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
# from fake_useragent import UserAgent
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.action_chains import ActionChains
# import uuid
#
# import logging
#
#
# class SeleniumScraper:
#     def __init__(self):
#         self.driver = None
#         self.init_driver()
#
#     def init_driver(self):
#         logging.warning('Open WebDriver')
#         user_agent = UserAgent().chrome
#         options = Options()
#         options.add_argument('--log-level=3')
#         # options.add_experimental_option('excludeSwitches', ['enable-logging'])
#         options.add_argument("--incognito")
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         options.add_argument("--disable-popup-blocking")
#         options.add_argument("--disable-notifications")
#         options.add_argument("--blink-settings=imagesEnabled=false")
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         options.add_argument('--start-maximized')
#         # options.add_argument('--headless')
#         options.add_argument(f'--user-agent={user_agent}')
#         self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="116.0.5845.96").install()),
#                                        options=options)
#
#     def click_element_by_class(self, class_name):
#         wait = WebDriverWait(self.driver, 10)
#         try:
#             element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
#             element.click()
#         except NoSuchElementException:
#             print(f"Element with class '{class_name}' not found.")
#
#     def click_element_by_xpath(self, xpath):
#         wait = WebDriverWait(self.driver, 10)
#         element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
#         element.click()
#         time.sleep(2)
#
#     def get_response(self, url):
#         # self.driver.get(url)
#         # page_source = self.driver.page_source
#         # return str(page_source)
#         max_retries = 3
#
#
#         retries = 0
#
#         while retries < max_retries:
#             try:
#                 self.driver.get(url)
#                 page_source = self.driver.page_source
#                 return str(page_source)
#             except Exception:
#                 retries += 1
#                 logging.warning(f"Timeout exception occurred for URL '{url}'. Retrying... (Attempt {retries})")
#
#         logging.warning(f"Max retries exceeded for URL '{url}'. Trying next URL...")
#
#         logging.warning(f"Unable to get response for all URLs.")
#         return None
#     def close_driver(self):
#         if self.driver:
#             self.driver.quit()
#             logging.warning('Close WebDriver')


import pprint
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
# from user_agent import generate_user_agent
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
        self.timer_start = None
        self.switch = False
        self.init_driver()

    def init_driver(self):
        logging.warning('Open WebDriver')
        # user_agent = UserAgent().chrome #TODO можно включить
        self.options = Options()
        self.options.add_argument('--log-level=3')
        # self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # self.options.add_argument("--incognito")#TODO не вариант, с ним криво работает
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument("--disable-popup-blocking")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--blink-settings=imagesEnabled=false")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--start-maximized')
        # self.options.add_argument('--headless') #TODO не вариант, с ним не работает
        # self.options.add_argument(f'--user-agent={user_agent}')#TODO можно оставить, я не стал устанавливать
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="116.0.5845.96").install()),
                                       options=self.options)
        # self.driver = webdriver.Chrome(options=self.options)
        while not self.switch:
            self.switch = self.switch_currency()
            logging.warning('Time-out')
        logging.warning("Successful switch currency")

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

    def refresh_page(self):
        self.driver.refresh()

    # def hover_over_element_by_class(self, x, y):
    #     actions = ActionChains(self.driver)
    #     actions.move_by_offset(x, y).perform()
    def get_response(self, url):
        self.driver.get(url)
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(self.driver)
        page_source = self.driver.page_source
        return str(page_source)

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            logging.warning('Close WebDriver')

    def reset_driver(self):
        self.driver.quit()
        time.sleep(2)
        self.driver = webdriver.Chrome(options=self.options)

    def check_timeout(self, time):
        return time - self.timer_start > 60

    def switch_currency(self):
        self.timer_start = time.time()
        while True:
            if self.check_timeout(time.time()):
                return

            link = (
                'https://www.alibaba.com/trade/search?spm=a2700.galleryofferlist.0.0.4bf33bdadf0Uyz&fsb=y&IndexArea=product_en&keywords=car+auction&tab=all&viewtype=G&&page=1')
            self.driver.get(link)
            try:
                ship_to = self.driver.find_element(By.XPATH,
                                                   '//*[@id="J_SC_header"]/header/div[4]/div/div[4]/div['
                                                   '5]/div/div/div[1]')
                logging.info('ship to find - ok')
                break
            except Exception:
                logging.warning('Incorrect site version. Reset driver')
                self.reset_driver()
                pass

        while True:
            if self.check_timeout(time.time()):
                return
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element_with_offset(ship_to, xoffset=10, yoffset=5).pause(2).click().perform()
                logging.info('ship to click - ok')
                break
            except Exception:
                pass

        while True:
            if self.check_timeout(time.time()):
                return
            try:
                country_input = self.driver.find_element(By.XPATH,
                                                         '//*[@id="J_SC_header"]/header/div[4]/div/div[4]/div['
                                                         '5]/div/div/div[2]/div[5]/div/div')
                logging.info('country_input find - ok')
                break
            except Exception:
                pass

        while True:
            if self.check_timeout(time.time()):
                return
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element_with_offset(country_input, xoffset=10, yoffset=5).pause(3).click().perform()
                logging.info('country_input click - ok')
                break
            except Exception:
                pass

        while True:
            if self.check_timeout(time.time()):
                return
            try:
                select_country = self.driver.find_element(By.XPATH,
                                                          '//*[@id="J_SC_header"]/header/div[4]/div/div[4]/div['
                                                          '5]/div/div/div[2]/div[5]/div/div/div[2]/ul/li[1]/ul/li[2]')
                logging.info('select_country find ok')
                break
            except Exception:
                pass
        while True:
            if self.check_timeout(time.time()):
                return
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element_with_offset(select_country, xoffset=10, yoffset=5).pause(3).click().perform()
                logging.info('select_country click ok')
                break
            except Exception:
                pass

        while True:
            if self.check_timeout(time.time()):
                return
            try:
                save_button = self.driver.find_element(By.XPATH,
                                                       '//*[@id="J_SC_header"]/header/div[4]/div/div[4]/div['
                                                       '5]/div/div/div[2]/div[6]/button')
                logging.info('save_button find ok')
                break
            except Exception:
                pass

        while True:
            if self.check_timeout(time.time()):
                return
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element_with_offset(save_button, xoffset=10, yoffset=5).pause(2).click().perform()
                logging.info('save_button click ok')
                return True
            except Exception:
                pass

# x = SeleniumScraper()
# input()
