import random
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..config.config import *
from ..config.assertion_config import *
from ..locators.lens_locators import LensLocators
from ..pages.map_page import MapPage
from time import sleep
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from ..pages.common import BasePage
from datetime import datetime
import time,os


class ServedPercentage(BasePage):
    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver


    def verify_served_percentage_actions(self):
        try:
            time.sleep(5)
            # Step 1: Verify Title
            title = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(LensLocators.SERVED_PERCENT_TITLE)
            )
            assert "Served" in title.text  # Adjust based on actual title
            print("[INFO] Title verified successfully.")

            # Step 2: Click Arrow Up Icon
            arrow_up = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(LensLocators.SERVED_PERCENT_ARROW_UP)
            )
            arrow_up.click()
            print("[INFO] Arrow Up button clicked.")

            # Step 3: Click Checkbox
            checkbox = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(LensLocators.SERVED_PERCENT_CHECKBOX)
            )
            if not checkbox.is_selected():
                checkbox.click()
                print("[INFO] Checkbox selected.")
            else:
                print("[INFO] Checkbox already selected.")

            try:
                # Wait for and attempt to click the opacity button
                opacity_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(LensLocators.SERVED_PERCENT_OPACITY)
                )
                try:
                    opacity_btn.click()
                    print("[INFO] Opacity button clicked.")
                except ElementClickInterceptedException:
                    print("[WARN] Click intercepted. Waiting for overlay to disappear...")
                    WebDriverWait(self.driver, 10).until(
                        EC.invisibility_of_element_located((By.ID, "service_coverage_no_data_row"))
                    )
                    opacity_btn.click()
                    print("[INFO] Opacity button clicked after overlay disappeared.")

                # Adjust Opacity Slider
                slider = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(LensLocators.SERVED_PERCENT_OPACITY_SLIDER)
                )
                ActionChains(self.driver).click_and_hold(slider).move_by_offset(-30, 0).release().perform()
                print("[INFO] Opacity slider adjusted.")

            except TimeoutException as e:
                print(f"[ERROR] Timeout while adjusting opacity: {e}")
            except Exception as e:
                print(f"[ERROR] Unexpected error during opacity adjustment: {e}")


            for index, toggle_locator in enumerate(LensLocators.SERVED_PERCENT_TOGGLE, start=1):
                toggle = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(toggle_locator)
                )
                toggle.click()
                print(f"[INFO] Toggled switch {index}.")

            return True

        except Exception as e:
            print(f"[ERROR] Served Percentage Lens verification failed: {e}")
            return False

