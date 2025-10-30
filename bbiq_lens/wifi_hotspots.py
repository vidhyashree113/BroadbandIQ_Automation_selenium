import random
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..config.config import *
from ..locators.lens_locators import LensLocators
from ..pages.map_page import MapPage
from ..pages.common import BasePage
from datetime import datetime
import time,os

class WifiLens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def click_wifi_lens(self):
        try:
            wifi_lens = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(LensLocators.WIFI_LENS_ICON)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", wifi_lens)
            time.sleep(1)
            try:
                wifi_lens.click()  # Try normal click
            except:
                self.driver.execute_script("arguments[0].click();", wifi_lens)  # JavaScript fallback
            print("[INFO] Wifi Hotspots lens clicked.")
        except Exception as e:
            print(f"[ERROR] Failed to click Wifi Hotspots lens: {e}")

    def verify_close_button_clickable(self):
        """Verify that the confirm button is clickable."""
        try:
            warning_text = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.WARNING_MESSAGE)
            )
            print(f'[INFO] : WARNING MESSAGE CAPTURED --> {warning_text.text}')
            confirm_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.CLOSE_BUTTON)
            )
            print("[INFO] Clicked on Confirm Button")
            confirm_button.click()
            return True
        except Exception as e:
            print(f"[ERROR] Confirm button is not clickable: {e}")
            return False

    def verify_lens_title(self):
        """Verify that the lens title is 'Wifi Hotspots' and return the result."""
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.LENS_TITLE_WIFI)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "WiFi Hotspots":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'WiFi Hotspots', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_wifi_lens_checkbox(self):
        """Verify that the wifi hotspots checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.WIFI_LEGEND_CHECKBOX)
            )
            if checkbox.is_selected():
                print("[INFO] WiFi Hotspots checkbox is checked.")
                return True
            else:
                print("[ERROR] WiFi Hotspots checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] WiFi Hotspots checkbox verification failed: {e}")
            return False