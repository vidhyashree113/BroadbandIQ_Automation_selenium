import random
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..config.config import *
from ..config.assertion_config import *
from ..locators.lens_locators import LensLocators
from ..pages.map_page import MapPage
from ..pages.common import BasePage
from datetime import datetime
import time,os

class UtilityLens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def click_utility_lens(self):
        try:
            utility_lens = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(LensLocators.UTILITY_LENS_ICON)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", utility_lens)
            time.sleep(1)
            try:
                utility_lens.click()  # Try normal click
            except:
                self.driver.execute_script("arguments[0].click();", utility_lens)  # JavaScript fallback
            print("[INFO] Utility Boundaries lens clicked.")
        except Exception as e:
            print(f"[ERROR] Failed to click Utility Boundaries lens: {e}")

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
            print("[INFO] Clicked on COnfirm button")
            confirm_button.click()
            return True
        except Exception as e:
            print(f"[ERROR] Confirm button is not clickable: {e}")
            return False

    def verify_lens_title(self):
        """Verify that the lens title is 'Utility Boundaries' and return the result."""
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.LENS_TITLE_UB)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "Utility Boundaries":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Utility Boundaries', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_utility_checkbox(self):
        """Verify that the Utility Boundaries checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.UB_LEGEND_CHECKBOX)
            )
            if checkbox.is_selected():
                print("[INFO] Utility Boundaries checkbox is checked.")
                return True
            else:
                print("[ERROR] Utility Boundaries checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] Utility Boundaries checkbox verification failed: {e}")
            return False

    # def randomly_toggle_two_switches(self):
    #     """Randomly turn OFF any 2 toggles while keeping others ON."""
    #     try:
    #         toggles_to_turn_off = random.sample(LensLocators.UTILITY_LENS_TOGGLE, 2)
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
    #         WebDriverWait(self.driver, 5).until(
    #             lambda driver: all(
    #                 driver.find_element(by, locator).is_enabled() for by, locator in toggles_to_turn_off
    #             )
    #         )
    #
    #         print("[PASSED] Random 2 toggles clicked successfully.")
    #         return True
    #
    #     except Exception as e:
    #         print(f"[ERROR] Failed to toggle switches: {e}")
    #         return False

    def toggle_off_all_switches_and_assert(self):
        """Turn OFF all Community Anchor toggles and assert label + state."""

        try:
            time.sleep(3)

            for index, (by, toggle_xpath) in enumerate(LensLocators.UTILITY_LENS_TOGGLE):
                # Click the toggle
                toggle_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((by, toggle_xpath))
                )
                toggle_element.click()
                label_text = UTILITY_BOUNDARIES_LABELS[index]
                print(f"[INFO] Clicked toggle {label_text}: {toggle_xpath}")

                label_xpath = f"(//div[@class='col-md-8']//span[normalize-space()='{label_text}'])[1]"
                label_element = self.driver.find_element(By.XPATH, label_xpath)

                # label_xpath = f"(//div[@class='color-legend-item']//span[normalize-space()='{label_text}'])[{1}]"
                # label_element = self.driver.find_element(By.XPATH, label_xpath)

                if not label_element.is_displayed():
                    print(f"[ERROR] Label not visible: '{label_text}'")
                    return False
                print(f"[INFO] Verified Actual and Expected Value : {label_text}")

                # Check if the toggle is OFF
                input_xpath = toggle_xpath.replace("span[@class='switch-slider round']", "input[@type='checkbox']")
                input_element = self.driver.find_element(By.XPATH, input_xpath)
                toggle_class = input_element.get_attribute("class")
                # print(f"[DEBUG] Toggle class for '{label_text}': {toggle_class}")

                if input_element.is_selected():
                    print(f"[ERROR] Toggle for '{label_text}' expected to be OFF, but it's ON!")
                    return False

            print("[PASSED] All toggles OFF with correct labels verified.")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to toggle or verify switches: {e}")
            return False

    def toggle_on_all_switches_and_assert(self):
        """
        Turn ON all toggles and assert they are ON by checking the absence of 'off-class' in the input tag.
        """
        try:
            toggles = LensLocators.UTILITY_LENS_TOGGLE
            labels = UTILITY_BOUNDARIES_LABELS

            for index, (by, span_locator) in enumerate(toggles):
                # Find the <span> and its corresponding <input>
                span_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((by, span_locator))
                )

                # Derive input_xpath based on known structure
                input_xpath = span_locator.replace("span[@class='switch-slider round']", "input[@type='checkbox']")
                input_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, input_xpath))
                )

                toggle_class = input_element.get_attribute("class")
                if not input_element.is_selected() and "off-class" in toggle_class:
                    span_element.click()
                    print(f"[INFO] Toggled ON: {labels[index]}")
                    time.sleep(1)
                else:
                    print(f"[INFO] Already ON: {labels[index]}")

            # Final assertion loop
            for index, (by, span_locator) in enumerate(toggles):
                input_xpath = span_locator.replace("span[@class='switch-slider round']", "input[@type='checkbox']")
                input_element = self.driver.find_element(By.XPATH, input_xpath)
                toggle_class = input_element.get_attribute("class")

                assert "off-class" not in toggle_class, f"[ERROR] {labels[index]} is still OFF!"
                print(f"[ASSERTION PASSED] {labels[index]} is ON ✅")

            return True

        except Exception as e:
            print(f"[ERROR] Failed to toggle ON all switches: {e}")
            return False

