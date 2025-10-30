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

class AreaBoundariesLens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def click_area_boundaries_lens(self):
        try:
            area_boundaries_lens = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(LensLocators.AREA_BOUNDARIES_LENS_ICON)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", area_boundaries_lens)
            time.sleep(1)
            try:
                area_boundaries_lens.click()  # Try normal click
            except:
                self.driver.execute_script("arguments[0].click();", area_boundaries_lens)  # JavaScript fallback
            print("[INFO] Area boundaries lens clicked.")
        except Exception as e:
            print(f"[ERROR] Failed to click Area Boundaries lens: {e}")

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
            print("[INFO] Clicking on Confirm button...")
            confirm_button.click()
            return True
        except Exception as e:
            print(f"[ERROR] Confirm button is not clickable: {e}")
            return False

    def verify_lens_title(self):
        """Verify that the lens title is 'Area Boundaries' and return the result."""
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.LENS_TITLE_AB)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "Area Boundaries":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Area Boundaries', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_area_boundaries_checkbox(self):
        """Verify that the Area Boundaries checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located(LensLocators.AB_LEGEND_CHECKBOX)
            )
            if checkbox.is_selected():
                print("[INFO] Area Boundaries checkbox is checked.")
                return True
            else:
                print("[ERROR] Area Boundaries checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] Area Boundaries checkbox verification failed: {e}")
            return False

    def toggle_on_all_except_municipal_city(self):
        """Toggle ON all layers except municipal and city which are already ON by default."""
        try:
            time.sleep(2)
            for index, (by, toggle_xpath) in enumerate(LensLocators.AREA_BOUNDARY_TOGGLE_OFF):  # only for specific 4
                input_element = self.driver.find_element(by, toggle_xpath)

                # Check if not checked initially
                if not input_element.get_attribute("checked"):
                    toggle_element = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((by, toggle_xpath.replace("input", "span")))
                    )
                    toggle_element.click()
                    print(f"[INFO] Toggled ON: {AREA_BOUNDARIES_LABELS_TOGGLE_OFF[index]}")

            print("[PASSED] All required toggles are turned ON.")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to toggle ON non-municipal/city toggles: {e}")
            return False

    def toggle_off_all_switches_and_assert(self):
        """Turn OFF all toggles, regardless of initial checked state or class."""
        try:
            time.sleep(2)

            for index, (by, toggle_xpath) in enumerate(LensLocators.AREA_BOUNDARY_TOGGLE):
                label_text = AREA_BOUNDARIES_LABELS[index]
                input_element = self.driver.find_element(by, toggle_xpath)

                if input_element.get_attribute("checked") or input_element.is_selected():
                    toggle_element = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((by, toggle_xpath.replace("input", "span")))
                    )
                    toggle_element.click()
                    print(f"[INFO] Toggled OFF: {label_text}")
                    time.sleep(1)

                # Confirm label is still visible
                label_xpath = f"(//div[@class='color-legend-item']//span[normalize-space()='{label_text}'])[1]"
                label_element = self.driver.find_element(By.XPATH, label_xpath)

                if not label_element.is_displayed():
                    print(f"[ERROR] Label not visible after toggle OFF: {label_text}")
                    return False

                print(f"[INFO] Verified label visibility after toggle OFF: {label_text}")

            print("[PASSED] All toggles turned OFF and verified.")
            return True

        except Exception as e:
            print(f"[ERROR] Failed while toggling OFF all switches: {e}")
            return False

    def toggle_on_all_switches_and_assert(self):
        """Turn ON all toggles, including those without off-class (e.g., congressional)."""
        try:
            time.sleep(2)

            for index, (by, toggle_xpath) in enumerate(LensLocators.AREA_BOUNDARY_TOGGLE):
                label_text = AREA_BOUNDARIES_LABELS[index]
                input_element = self.driver.find_element(by, toggle_xpath)

                if not input_element.is_selected():
                    toggle_element = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((by, toggle_xpath.replace("input", "span")))
                    )
                    toggle_element.click()
                    print(f"[INFO] Toggled ON: {label_text}")
                    time.sleep(1)

                # Confirm label is visible
                label_xpath = f"(//div[@class='color-legend-item']//span[normalize-space()='{label_text}'])[1]"
                label_element = self.driver.find_element(By.XPATH, label_xpath)

                if not label_element.is_displayed():
                    print(f"[ERROR] Label not visible after toggle ON: {label_text}")
                    return False

            print("[PASSED] All toggles turned ON and verified.")
            return True

        except Exception as e:
            print(f"[ERROR] Failed while toggling ON all switches: {e}")
            return False



    def toggle_off_all_except(self, keep_label):
        """
        Turns OFF all toggles *except* the one matching `keep_label`.
        """
        try:
            for label, (by, span_xpath) in LensLocators.AREA_BOUNDARIES_TOGGLES.items():
                input_xpath = span_xpath.replace(
                    "span[@class='switch-slider round']", "input[@type='checkbox']"
                )
                input_element = self.driver.find_element(By.XPATH, input_xpath)

                # Skip the one we want to keep ON
                if label == keep_label:
                    continue

                toggle_class = input_element.get_attribute("class")
                if "off-class" in toggle_class:
                    print(f"[INFO] {label} already OFF ✅")
                    continue

                try:
                    span_element = self.driver.find_element(by, span_xpath)
                    try:
                        span_element.click()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", span_element)
                        print(f"[INFO] JS fallback click used for {label}")

                    WebDriverWait(self.driver, 10).until(
                        lambda d: "off-class" in d.find_element(By.XPATH, input_xpath).get_attribute("class")
                                  or not d.find_element(By.XPATH, input_xpath).is_selected()
                    )

                    toggle_class_after = input_element.get_attribute("class")
                    if "off-class" not in toggle_class_after:
                        print(f"[ERROR] Toggle '{label}' still ON!")
                        return False

                    print(f"[INFO] Turned OFF: {label}")

                except Exception as inner_e:
                    print(f"[ERROR] Couldn't toggle OFF '{label}': {inner_e}")
                    self.take_screenshot(f"toggle_off_except_failed_{label}")
                    return False

            print(f"[✅ PASSED] All toggles OFF except: {keep_label}")
            return True

        except Exception as e:
            print(f"[ERROR] toggle_off_all_except failed: {e}")
            self.take_screenshot("toggle_off_all_except_error")
            return False