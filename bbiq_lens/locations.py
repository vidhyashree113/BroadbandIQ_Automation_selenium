import random
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..config.assertion_config import LOCATION_LENS_LABELS
from ..config.config import *
from ..locators.lens_locators import LensLocators
from ..pages.map_page import MapPage
from ..pages.common import BasePage
from datetime import datetime
import time,os

class LocationLens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def click_locations_lens(self):
        try:
            location_lens = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(LensLocators.Locations_lens)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", location_lens)
            time.sleep(2)
            try:
                location_lens.click()  # Try normal click

            except:
                self.driver.execute_script("arguments[0].click();", location_lens)  # JavaScript fallback
                print("[INFO] Locations Boundaries lens clicked.")

        except Exception as e:
            print(f"[ERROR] Failed to click Locations Boundaries lens: {e}")

    def verify_close_button_clickable(self):
        """Verify that the confirm button is clickable."""
        try:
            warning_text = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.WARNING_MESSAGE)
            )
            print(f'[INFO] : WARNING MESSAGE CAPTURED --> {warning_text.text}')
            confirm_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.Locations_close)
            )

            print("[INFO] Clicked on Confirm button")
            confirm_button.click()
            return True

        except Exception as e:
            print(f"[ERROR] Confirm button is not clickable: {e}")
            return False


    def verify_lens_title(self):

        try:

            lens_title_element = WebDriverWait(self.driver,30).until(EC.visibility_of_element_located(LensLocators.Lens_title_loc))

            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == lens_title_element.text.strip():
                return True

            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Locations', Found: '{title_text}'")
                return False

        except Exception as msg:
            print(f"[ERROR] Lens title verification failed: {msg}")
            return False


    def verify_location_checkbox(self):
        """Verify that the Household Income checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.Lens_legend_checkbox_loc)
            )
            if checkbox.is_selected():
                print("[INFO] checkbox is checked.")
                return True
            else:
                print("[ERROR] Location lens checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] Location lens checkbox verification failed: {e}")
            return False


    # def randomly_toggle_two_switches(self):
    #     """Randomly turn OFF any 2 toggles while keeping others ON."""
    #     try:
    #         toggles_to_turn_off = random.sample(LensLocators.Locations_lens_Toggle, 2)
    #         print(f"[INFO] Selected toggles to turn off: {toggles_to_turn_off}")
    #
    #         for by, locator in toggles_to_turn_off:
    #             toggle_element = WebDriverWait(self.driver, 10).until(
    #                 EC.element_to_be_clickable((by, locator))
    #             )
    #             toggle_element.click()
    #             print(f"[INFO] Clicked toggle: {locator}")
    #
    #         # **Ensure toggles are clicked before proceeding**
    #         # WebDriverWait(self.driver, 5).until(
    #         #     lambda driver: all(
    #         #         driver.find_element(by, locator).is_enabled() for i,j  in toggles_to_turn_off
    #         #     )
    #         # )
    #
    #             print("[PASSED] Random 2 toggles clicked successfully.")
    #             return True
    #
    #     except Exception as e:

    def toggle_off_all_switches_and_assert(self):
        """Turn OFF all toggles and assert label + state."""

        try:
            time.sleep(5)

            for index, (by, toggle_xpath) in enumerate(LensLocators.Locations_lens_Toggle):
                # Click the toggle
                toggle_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((by, toggle_xpath))
                )
                toggle_element.click()
                label_text = LOCATION_LENS_LABELS[index]
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
            toggles = LensLocators.Locations_lens_Toggle
            labels = LOCATION_LENS_LABELS

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

    def verify_commercial_filter(self):
        """Verify that the los filter is clicked"""
        try:
            time.sleep(5)
            filter_button = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.LOCATION_COMMERCIAL_FILTER)
            )
            filter_button.click()
            print("[INFO] Location Commerical filter is clicked.")

            # slider button sliding

            slider = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.LOCATION_COMMERCIAL_SLIDER)
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", slider)
            time.sleep(1)

            # Drag the slider (you can adjust the offset based on expected value)
            actions = ActionChains(self.driver)
            actions.click_and_hold(slider).move_by_offset(20, 0).release().perform()
            print("[INFO] Slider adjusted.")
            time.sleep(3)
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(LensLocators.LOCATION_FILTER_SUBMIT))
            # print("[DEBUG] Clicking Submit button")
            submit_button.click()
            # print("[DEBUG] Submit clicked. Waiting for result...")
            print("[INFO] Location Commercial filter Submit button clicked.")
            return True

        except Exception as e:
            print(f"Error in Location Commercial filter workflow: {e}")
            return False