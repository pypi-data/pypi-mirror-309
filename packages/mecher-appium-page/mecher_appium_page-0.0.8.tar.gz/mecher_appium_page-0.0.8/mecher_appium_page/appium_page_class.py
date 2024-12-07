import logging

import allure
from appium.webdriver.webdriver import WebDriver

from mecher_appium_page.models.app_config import AppConfig
from selenium.webdriver.support.wait import WebDriverWait

from mecher_appium_page.models.locators import AppiumLocators


class AppiumPage():
    def __init__(self,
                 driver_appium: WebDriver,
                 app_config: AppConfig,
                 locators: AppiumLocators):
        self.logger = logging.getLogger(__name__)

        self.driver_appium = driver_appium
        self.wait = WebDriverWait(self.driver_appium, app_config.WAIT_FOR_ELEMENT_TIMEOUT)
        self.app_config = app_config

        self.locators = locators

    def press_back_btn(self):
        with allure.step('Press system "back" button'):
            self.logger.info('Press system "back" button')
            self.driver_appium.back()
