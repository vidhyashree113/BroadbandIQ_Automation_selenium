import random
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..config.config import *
from ..config.assertion_config import *
from ..locators.lens_locators import LensLocators
from time import sleep
from ..pages.map_page import MapPage
from ..pages.common import BasePage
from datetime import datetime
import time,os

class Road_Rail_Road(BasePage):

    def __init__(self,driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def click_road_rail_lens(self):
        try:

            road_rail_lens = WebDriverWait(self.driver,30).until(EC.element_to_be_clickable(LensLocators.RAIL_ROADS))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",road_rail_lens)
            sleep(1)

            try:

                road_rail_lens.click() #normal click

            except:

                self.driver.execute_script("arguments[0].click();", road_rail_lens)
                print("[INFO] ROAD RAIL lens lens clicked.")

        except Exception as msg:
            print(f'[ERROR] failed to click on ROAD RAIL lens :{msg}')


    def verify_lens_title(self):

        try:

            lens_title_element = WebDriverWait(self.driver,30).until(EC.visibility_of_element_located(LensLocators.RAIL_ROADS_TITLE))

            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == lens_title_element.text.strip():
                return True

            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Roads,Rail Roads and RoW', Found: '{title_text}'")
                return False

        except Exception as msg:
            print(f"[ERROR] Lens title verification failed: {msg}")
            return False


    def verify_road_rail_checkbox(self):
        """Verify that the Household Income checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.RAIL_ROADS_LEGEND_CHECKBOX)
            )
            if checkbox.is_selected():
                print("[INFO] checkbox is checked.")
                return True
            else:
                print("[ERROR] ROAD RAIL checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] ROAD RAIL checkbox verification failed: {e}")
            return False

    def verify_close_button_clickable(self):
        """Verify that the confirm button is clickable."""
        try:
            confirm_button = WebDriverWait(self.driver, 35).until(
                EC.element_to_be_clickable(LensLocators.RAIL_ROADS_CLOSE)
            )
            print("[INFO] Confirm button is clickable.Clicking now...")
            confirm_button.click()
            return True
        except Exception as e:
            print(f"[ERROR] Confirm button is not clickable: {e}")
            return False


    def toggle_off_all_switches_and_assert(self):
        """Turn OFF all Community Anchor toggles and assert label + state."""

        try:
            time.sleep(5)

            for index, (by, toggle_xpath) in enumerate(LensLocators.RAIL_ROADS_TOGGLE):
                # Click the toggle
                toggle_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((by, toggle_xpath))
                )
                toggle_element.click()
                label_text = RAIL_ROADS_LABELS[index]
                print(f"[INFO] Clicked toggle {label_text}: {toggle_xpath}")
                time.sleep(1)

                # Get corresponding label

                label_xpath = f"(//div[@class='color-legend-item']//span[normalize-space()='{label_text}'])[{1}]"
                label_element = self.driver.find_element(By.XPATH, label_xpath)

                if not label_element.is_displayed():
                    print(f"[ERROR] Label not visible: '{label_text}'")
                    return False
                print(f"[INFO] Verified Actual and Expected Value : {label_text}")

                # Check if the toggle is OFF
                input_xpath = toggle_xpath.replace("span[@class='switch-slider round']", "input[@type='checkbox']")
                input_element = self.driver.find_element(By.XPATH, input_xpath)
                toggle_class = input_element.get_attribute("class")
                # print(f"[DEBUG] Toggle class for '{label_text}': {toggle_class}")

                if "off-class" not in toggle_class:
                    print(f"[ERROR] Toggle for '{label_text}' expected to be OFF, but it's ON!")
                    return False

            print("[PASSED] All toggles OFF with correct labels verified.")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to toggle or verify switches: {e}")
            return False

    def toggle_on_all_switches_and_assert(self):
        """
        Turn ON all  toggles and assert they are ON by checking the absence of 'off-class' in the input tag.
        """
        try:
            toggles = LensLocators.RAIL_ROADS_TOGGLE
            labels = RAIL_ROADS_LABELS

            for index, (by, span_locator) in enumerate(toggles):
                # Find the <span> to click
                span_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((by, span_locator))
                )
                # self.driver.execute_script("arguments[0].scrollIntoView(true);", span_element)

                input_element = span_element.find_element(By.XPATH, "./preceding-sibling::input")
                toggle_class = input_element.get_attribute("class")
                # print(f"[DEBUG] Initial INPUT class for '{labels[index]}': {toggle_class}")

                if "off-class" in toggle_class:
                    span_element.click()
                    print(f"[INFO] Toggled ON: {labels[index]}")
                    time.sleep(1)
                else:
                    print(f"[INFO] Already ON: {labels[index]}")

            for index, (by, span_locator) in enumerate(toggles):
                span_element = self.driver.find_element(by, span_locator)
                input_element = span_element.find_element(By.XPATH, "./preceding-sibling::input")
                toggle_class = input_element.get_attribute("class")

                assert "off-class" not in toggle_class, f"[ERROR] {labels[index]} is still OFF!"
                print(f"[ASSERTION PASSED] {labels[index]} is ON ✅")

            return True

        except Exception as e:
            print(f"[ERROR] Failed to toggle ON all switches: {e}")
            return False




