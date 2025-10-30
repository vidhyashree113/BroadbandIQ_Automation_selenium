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

class DataCentreLocationLens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def click_dcl_lens(self):
        try:
            dcl_lens = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(LensLocators.Data_centre_locations_lens)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dcl_lens)
            time.sleep(1)
            try:
                dcl_lens.click()  # Try normal click
            except:
                self.driver.execute_script("arguments[0].click();", dcl_lens)  # JavaScript fallback
            print("[INFO] Data Centre Locations Boundaries lens clicked.")
        except Exception as e:
            print(f"[ERROR] Failed to clickData Centre Locations  Boundaries lens: {e}")

    def verify_close_button_clickable(self):
        """Verify that the confirm button is clickable."""
        try:
            warning_text = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.WARNING_MESSAGE)
            )
            print(f'[INFO] : WARNING MESSAGE CAPTURED --> {warning_text.text}')
            confirm_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.Data_centre_close)
            )
            print("[INFO] Clicking on Confirm button")
            confirm_button.click()
            return True
        except Exception as e:
            print(f"[ERROR] Confirm button is not clickable: {e}")
            return False

    def verify_lens_title(self):
        """Verify that the lens title is 'Data Centre  Boundaries' and return the result."""
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.Lens_title_DCL)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "Data Center Locations":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Data Center Locations', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_dcl_lens_checkbox(self):
        """Verify that the Data centre Boundaries checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.DCL_legend_checkbox)
            )
            if checkbox.is_selected():
                print("[INFO] DCL Boundaries checkbox is checked.")
                return True
            else:
                print("[ERROR] DCL Boundaries checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] DCL Boundaries checkbox verification failed: {e}")
            return False

    # def grant_opportunity_opacity(self, offset):
    #     try:
    #         time.sleep(3)
    #         # **Wait for opacity button to be clickable**
    #         print("[INFO] Waiting for opacity button...")
    #         time.sleep(3)
    #         opacity_button3 = WebDriverWait(self.driver, 30).until(
    #             EC.element_to_be_clickable(LensLocators.Opacity_GO)
    #         )
    #         print("[INFO] Opacity button found, clicking...")
    #         opacity_button3.click()
    #
    #         # **Ensure the slider is present & visible**
    #         print("[INFO] Waiting for opacity slider...")
    #         opacity_slider3 = WebDriverWait(self.driver, 30).until(
    #             EC.visibility_of_element_located(LensLocators.Opacity_slider_GO)
    #         )
    #         print("[INFO] Opacity slider found.")
    #
    #         # **Ensure slider is interactable before moving**
    #         WebDriverWait(self.driver, 10).until(
    #             EC.element_to_be_clickable(LensLocators.Opacity_slider_GO)
    #         )
    #         print("[INFO] Opacity slider is clickable.")
    #
    #         # **Perform drag action**
    #         actions = ActionChains(self.driver)
    #         actions.move_to_element(opacity_slider3).click_and_hold().move_by_offset(offset, 0).release().perform()
    #         print(f"[INFO] Opacity adjusted by offset: {offset}")
    #
    #         return True  # **Return success**
    #
    #     except Exception as e:
    #         print(f"[ERROR] Failed to adjust opacity: {e}")
    #         return False
    #
    # def randomly_toggle_two_switches(self):
    #     """Randomly turn OFF any 2 toggles while keeping others ON."""
    #
    #     try:
    #         time. sleep(3)
    #         toggles_to_turn_off = random.sample(LensLocators.Grant_Opportunity_Lens_Toggle, 2)
    #         print(f"[INFO] Selected toggles to turn off: {toggles_to_turn_off}")
    #
    #         for by, locator in toggles_to_turn_off:
    #             toggle_element = WebDriverWait(self.driver, 10).until(
    #                 EC.element_to_be_clickable((by, locator))
    #             )
    #             toggle_element.click()
    #             print(f"[INFO] Clicked toggle: {locator}")
    #             time.sleep(2)
    #
    #         # **Ensure toggles are clicked before proceeding**
    #         WebDriverWait(self.driver, 10).until(
    #             lambda driver: all(
    #                 driver.find_element(by, locator).is_enabled() for i, j in toggles_to_turn_off
    #             )
    #         )
    #
    #         print("[PASSED] Random 2 toggles clicked successfully.")
    #         return True
    #
    #
    #     except Exception as e:
    #         print(f"[ERROR] Failed to toggle switches: {e}")
    #         return False