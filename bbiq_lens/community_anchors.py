import random

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..config.assertion_config import *
from ..locators.lens_locators import LensLocators
from ..pages.map_page import MapPage
from ..pages.common import BasePage
from datetime import datetime
import time,os

class CommunityLens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver


    def click_community_lens(self):
        try:
            community_lens = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(LensLocators.Community_Anchor_lens)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", community_lens)
            time.sleep(2)
            try:
                community_lens.click()  # Try normal click

            except:
                self.driver.execute_script("arguments[0].click();", community_lens)  # JavaScript fallback
                print("[INFO] COMMUNITY ANCHOR Boundaries lens clicked.")

        except Exception as e:
            print(f"[ERROR] Failed to click COMMUNITY ANCHOR Boundaries lens: {e}")

    def verify_close_button_clickable(self):
        """Verify that the confirm button is clickable."""
        try:
            warning_text = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.WARNING_MESSAGE)
            )
            print(f'[INFO] : WARNING MESSAGE CAPTURED --> {warning_text.text}')
            confirm_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.Community_Anchor_close)
            )

            print("[INFO] Clicking on Confirm button...")
            time.sleep(2)
            confirm_button.click()
            return True

        except Exception as e:
            print(f"[ERROR] Confirm button is not clickable: {e}")
            return False

    def verify_lens_title(self):
        """Verify that the lens title is 'Community OPPORTUNITY  Boundaries' and return the result."""
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.Lens_title_CA)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "Community Anchor Institutions":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'COMMUNITY ANCHOR', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_community_lens_checkbox(self):
        """Verify that the GRANT Boundaries checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.Lens_legend_checkbox_CA)
            )
            if checkbox.is_selected():
                print("[INFO] COMMUNITY Boundaries checkbox is checked.")
                return True
            else:
                print("[ERROR] COMMUNITY Boundaries checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] COMMUNITY Boundaries checkbox verification failed: {e}")
            return False

    def download_csv(self):
        try:
            time.sleep(10)
            # Wait for and click the Export button
            export = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable(LensLocators.Export_button)
            )
            export.click()

            # Wait for and interact with the file name input
            file_name_input = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(LensLocators.File_name)
            )
            file_name_input.clear()

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f'Community_lens_{timestamp}'
            file_name_input.send_keys(file_name)
            # Avoid hard-coded sleep if possible
            # time.sleep(4) → Prefer waiting for Submit to be clickable
            submit_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.Submit)
            )
            submit_button.click()
            return True

        except TimeoutException as te:
            print(f"[TIMEOUT] Element not found or clickable in time: {te}")
            # Take screenshot for debugging
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f'csv_download_error_{timestamp}'
            self.take_screenshot(file_name)
            return False

        except Exception as e:
            print(f"[ERROR] Failed to download csv: {e}")
            # Optional: take screenshot here too
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f'csv_download_error_{timestamp}'
            self.take_screenshot(file_name)
            return False

    def toggle_off_all_switches_and_assert(self):
        """Turn OFF all Community Anchor toggles and assert label + state."""

        try:
            time.sleep(3)

            for index, (by, toggle_xpath) in enumerate(LensLocators.Community_Anchor_Lens_Toggle):
                # Click the toggle
                toggle_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((by, toggle_xpath))
                )
                toggle_element.click()
                label_text = COMMUNITY_ANCHOR_LABELS[index]
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
        Turn ON all community anchor toggles and assert they are ON by checking the absence of 'off-class' in the input tag.
        """
        try:
            toggles = LensLocators.Community_Anchor_Lens_Toggle
            labels = COMMUNITY_ANCHOR_LABELS

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