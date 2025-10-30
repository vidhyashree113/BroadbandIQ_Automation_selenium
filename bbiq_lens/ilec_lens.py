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

class IlecLens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def click_ilec_lens(self):
        try:
            ilec_lens = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(LensLocators.ILEC_LENS_ICON)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ilec_lens)
            time.sleep(1)
            try:
                ilec_lens.click()  # Try normal click
            except:
                self.driver.execute_script("arguments[0].click();", ilec_lens)  # JavaScript fallback
            print("[INFO] ILEC Boundaries lens clicked.")
        except Exception as e:
            print(f"[ERROR] Failed to click ILEC Boundaries lens: {e}")

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
        """Verify that the lens title is 'ILEC Boundaries' and return the result."""
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.LENS_TITLE_IL)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "ILEC Boundaries":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'ILEC Boundaries', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_ilec_lens_checkbox(self):
        """Verify that the ILEC Boundaries checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.IL_LEGEND_CHECKBOX)
            )
            if checkbox.is_selected():
                print("[INFO] ILEC Boundaries checkbox is checked.")
                return True
            else:
                print("[ERROR] ILEC Boundaries checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] ILEC Boundaries checkbox verification failed: {e}")
            return False