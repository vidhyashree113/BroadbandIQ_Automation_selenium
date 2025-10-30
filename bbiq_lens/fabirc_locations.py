import random
import re

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

class FabricLens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def click_fabric_location_lens(self):
        try:
            fabric_lens = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(LensLocators.FABRIC_LENS)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", fabric_lens)
            time.sleep(1)
            try:
                fabric_lens.click()  # Try normal click
            except:
                self.driver.execute_script("arguments[0].click();", fabric_lens)  # JavaScript fallback
            print("[INFO] Fabric Location lens clicked.")
        except Exception as e:
            print(f"[ERROR] Failed to click Fabric Location lens: {e}")

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
            print("[INFO] Clicked on Confirm Button...")
            confirm_button.click()
            return True
        except Exception as e:
            print(f"[ERROR] Confirm button is not clickable: {e}")
            return False

    def verify_lens_title(self):
        """Verify that the lens title is 'Area Boundaries' and return the result."""
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.FABRIC_LOCATION_TITLE)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "Fabric Locations":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Fabric Locations', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_fabric_location_checkbox(self):
        """Verify that the Area Boundaries checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located(LensLocators.FABRIC_LOCATION_CHECKBOX)
            )
            if checkbox.is_selected():
                print("[INFO] Fabric Location checkbox is checked.")
                return True
            else:
                print("[ERROR] Fabric Location checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] Fabric Location checkbox verification failed: {e}")
            return False

    def verify_toggle_off_all_except_underserved_unserved(self):
        """Toggle ON all layers except municipal and city which are already ON by default."""
        try:
            time.sleep(2)
            for index, (by, toggle_xpath) in enumerate(LensLocators.FABRIC_LOCATION_TOGGLE_OFF):  # only for specific 4
                input_element = self.driver.find_element(by, toggle_xpath)

                # Check if not checked initially
                if not input_element.get_attribute("checked"):
                    toggle_element = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((by, toggle_xpath.replace("input", "span")))
                    )
                    toggle_element.click()
                    print(f"[INFO] Toggled OFF: {FABRIC_LOCATION_LABELS_TOGGLE_OFF[index]}")

            print("[PASSED] All required toggles are turned OFF.")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to toggle OFF residential/business/Institutional toggles: {e}")
            return False

    def toggle_off_all_switches_and_assert(self):
        """Turn OFF all toggles, regardless of initial checked state or class."""
        try:
            time.sleep(2)

            for index, (by, toggle_xpath) in enumerate(LensLocators.FABRIC_LOCATION_TOGGLE):
                label_text = FABRIC_LOCATION_LABELS[index]
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

    import re
    import time

    def extract_count_from_label(self,label_text: str) -> int:
        """Extract numeric count from a label like 'Unserved (4,874)'."""
        match = re.search(r'\(([\d,]+)\)', label_text)
        if match:
            return int(match.group(1).replace(',', ''))
        return 0

    def toggle_on_all_switches_and_assert(self):
        """Toggle ON all Fabric Location toggles and extract count from labels like 'Unserved (4,874)'."""
        try:
            time.sleep(2)

            for index, (by, toggle_xpath) in enumerate(LensLocators.FABRIC_LOCATION_TOGGLE):
                label_text = FABRIC_LOCATION_LABELS[index]

                input_element = self.driver.find_element(by, toggle_xpath)

                if not input_element.is_selected():
                    toggle_element = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((by, toggle_xpath.replace("input", "span")))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", toggle_element)
                    toggle_element.click()
                    print(f"[INFO] Toggled ON: {label_text}")
                    time.sleep(1)
                else:
                    print(f"[INFO] Already ON: {label_text}")

                # Use contains() in case label has dynamic count like 'Unserved (4,874)'
                label_xpath = f"(//div[@class='color-legend-item']//span[contains(normalize-space(), '{label_text}')])[1]"

                try:
                    label_element = WebDriverWait(self.driver, 5).until(
                        EC.visibility_of_element_located((By.XPATH, label_xpath))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", label_element)
                    label_text_with_count = label_element.text
                    count = self.extract_count_from_label(label_text_with_count)

                    print(f"[INFO] Count for {label_text}: {count}")

                    # Optional: Validate against expected count
                    if label_text in EXPECTED_COUNTS:
                        expected = EXPECTED_COUNTS[label_text]
                        assert count == expected, f"[ERROR] Count mismatch for {label_text}: expected {expected}, got {count}"

                except Exception:
                    print(f"[ERROR] Label not visible or failed to extract count for: {label_text}")
                    return False

            print("[PASSED] All toggles turned ON and counts verified.")
            return True

        except Exception as e:
            print(f"[ERROR] Failed while toggling ON all switches: {e}")
            return False

    def verify_default_off_toggles(self):
        """
        Verify 'Unserved' and 'Underserved' toggles are OFF (unchecked) by default.
        """
        try:
            failed_labels = []

            for label in FABRIC_LOCATION_LABELS_DEFAULT_OFF:
                by, xpath = LensLocators.FABRIC_LOCATION_TOGGLE_DEAFULT_OFF[label]
                input_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((by, xpath))
                )
                is_checked = input_element.get_attribute("checked")

                if is_checked:
                    print(f"[ERROR] Toggle '{label}' is ON by default.")
                    failed_labels.append(label)
                else:
                    print(f"[INFO] Toggle '{label}' is OFF by default.")

            if failed_labels:
                print(f"[FAILED] Toggles ON by default: {failed_labels}")
                return False

            return True

        except Exception as e:
            print(f"[ERROR] Exception during toggle verification: {e}")
            return False

    # def toggle_on_all_switches_and_assert(self):
    #     """Turn ON all toggles, including those without off-class (e.g., congressional)."""
    #     try:
    #         time.sleep(2)
    #
    #         for index, (by, toggle_xpath) in enumerate(LensLocators.FABRIC_LOCATION_TOGGLE):
    #             label_text = FABRIC_LOCATION_LABELS[index]
    #             input_element = self.driver.find_element(by, toggle_xpath)
    #
    #             if not input_element.is_selected():
    #                 toggle_element = WebDriverWait(self.driver, 10).until(
    #                     EC.element_to_be_clickable((by, toggle_xpath.replace("input", "span")))
    #                 )
    #                 toggle_element.click()
    #                 print(f"[INFO] Toggled ON: {label_text}")
    #                 time.sleep(1)
    #
    #             # Confirm label is visible
    #             label_xpath = f"(//div[@class='color-legend-item']//span[normalize-space()='{label_text}'])[1]"
    #             label_element = self.driver.find_element(By.XPATH, label_xpath)
    #
    #             if not label_element.is_displayed():
    #                 print(f"[ERROR] Label not visible after toggle ON: {label_text}")
    #                 return False
    #
    #         print("[PASSED] All toggles turned ON and verified.")
    #         return True
    #
    #     except Exception as e:
    #         print(f"[ERROR] Failed while toggling ON all switches: {e}")
    #         return False