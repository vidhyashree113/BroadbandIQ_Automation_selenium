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
# import time

class Lcp_Lens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def click_lcp_lens(self):
        try:
            lcp_lens = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(LensLocators.LCP_LENS)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", lcp_lens)
            time.sleep(1)
            try:
                lcp_lens.click()  # Try normal click
            except:
                self.driver.execute_script("arguments[0].click();", lcp_lens)  # JavaScript fallback
            print("[INFO] : LCP Lens clicked.")
        except Exception as e:
            print(f"[ERROR] Failed to click HotWire lens: {e}")

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
            print("[INFO] : Clicked on Confirm button...")
            confirm_button.click()
            return True
        except Exception as e:
            print(f"[ERROR] Confirm button is not clickable: {e}")
            return False

    def verify_lens_title(self):
        """Verify that the lens title is 'Area Boundaries' and return the result."""
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.LCP_LENS_TITLE)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "Lean Corporate Partners (LCP)":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Lean Corporate Partners (LCP)', Found: '{title_text}'")
                return False
            #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_lcp_lens_checkbox(self):
        """Verify that the Area Boundaries checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located(LensLocators.LCP_LENS_CHECKBOX)
            )
            if checkbox.is_selected():
                print("[INFO] LCP LENS checkbox is checked.")
                return True
            else:
                print("[ERROR] LCP LENS checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] LCP LENS checkbox verification failed: {e}")
            return False

    def toggle_on_all_switches_and_assert(self):
        """
        Turn ON all  toggles and assert they are ON by checking the absence of 'off-class' in the input tag.
        """
        try:
            toggles = LensLocators.LCP_LENS_TOGGLE
            labels = LCP_TOGGLE_LABEL

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


    def toggle_off_all_switches_and_assert(self):
        """Turn OFF all toggles, regardless of initial checked state or class."""

        try:
            time.sleep(5)
            for index, (by, toggle_xpath) in enumerate(LensLocators.LCP_LENS_TOGGLE):
                label_text = LCP_TOGGLE_LABEL[index]
                # Click the toggle
                toggle_element = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((by, toggle_xpath))
                )
                toggle_element.click()
                # label_text = CELL_TOWERS_LABELS[index]

                # print(f"[INFO] Clicked toggle OFF for {label_text}: {toggle_xpath}")
                print(f"[INFO] Clicked toggle OFF for {label_text}")
                time.sleep(1)

                # Get corresponding label

                label_xpath = f"(//div[@class='color-legend']//span[normalize-space()='{label_text}'])"
                label_element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, label_xpath))
                )

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


    def capturing_warning_message(self):
        try:
            toast_element = self.wait_for_element(LensLocators.LCP_LENS_TOAST_MESSAGE)
            print(f'[INFO] : CONFIRMATION MESSAGE - {toast_element.text}')
            return True
        except Exception as e:
            print(f'[ERROR] : FAILED TO CAPTURE ERROR MESSAGE')
            return False