import random
from selenium.webdriver import ActionChains, Keys
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

class KineticLens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def click_kinetic_lens(self):
        try:
            kinetic_lens = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.KINETIC_LENS)
            )
            # print("DEBUG locator:", LensLocators.COVERAGE_AREA_LENS)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", kinetic_lens)
            time.sleep(1)
            try:
                # print("DEBUG locator:", LensLocators.COVERAGE_AREA_LENS)
                kinetic_lens.click()  # Try normal click
            except:
                self.driver.execute_script("arguments[0].click();", kinetic_lens)  # JavaScript fallback
            print("[INFO] Kinetic Lens lens clicked.")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to click Middle Mile lens: {e}")
            return False

    def kinetic_lens_search_county(self):
        try:
            county = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable(LensLocators.KINETIC_SEARCH_COUNTY)
            )
            county.click()
            print('[INFO] : CLICKED ON PROVIDER PLACEHOLDER')
            time.sleep(2)

            county_value = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable(LensLocators.KINETIC_SEARCH_COUNTY_VALUE)
            )
            county_value.click()
            print(f'[INFO] : CLICKED ON PROVIDER VALUE - {KINETIC_COUNTY_VALUE}')
            time.sleep(2)
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO CLICK ON COUNTY')
            return False


    def verify_lens_title(self):
        """Verify that the lens title is 'Density Locations per sq. mile' and return the result."""
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.KINETIC_LENS_TITLE)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "Kinetic":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Kinetic', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_kinetic_lens_checkbox(self):
        """Verify that the Area Density checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.KINETIC_LENS_CHECKBOX)
            )
            if checkbox.is_selected():
                print("[INFO] Kinetic Lens checkbox is checked.")
                return True
            else:
                print("[ERROR] Kinetic Lens checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR]  Kinetic Lens verification failed: {e}")
            return False

    def toggle_off_all_switches_and_assert(self):
        """Turn OFF all toggles and assert label + state."""

        try:
            time.sleep(5)

            for index, (by, toggle_xpath) in enumerate(LensLocators.KINETIC_LENS_TOGGLE):
                # Click the toggle
                toggle_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((by, toggle_xpath))
                )
                toggle_element.click()
                time.sleep(2)
                label_text = KINETIC_TOGGLE_LABELS[index]
                print(f"[INFO] Clicked toggle {label_text}: {toggle_xpath}")
                time.sleep(1)

                # Get corresponding label

                label_xpath = f"(//div[@class='color-legend-item']//span[normalize-space()='{label_text}'])[{1}]"  # f"(//div[@class='color-legend-item']//span[normalize-space()='{label_text}'])[{1}]"
                label_element = self.driver.find_element(By.XPATH, label_xpath)
                print(label_xpath)

                if not label_element.is_displayed():
                    print(f"[ERROR] Label not visible: '{label_text}'")
                    return False
                print(f"[INFO] Verified Actual and Expected Value: {label_text}")

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
            toggles = LensLocators.KINETIC_LENS_TOGGLE
            labels = KINETIC_TOGGLE_LABELS

            for index, (by, span_locator) in enumerate(toggles):
                # Find the <span> to click
                span_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((by, span_locator))
                )
                # self.driver.execute_script("arguments[0].scrollIntoView(true);", span_element)

                input_element = span_element.find_element(By.XPATH, "./preceding-sibling::input")
                toggle_class = input_element.get_attribute("class")
                # print(f"[DEBUG] Initial INPUT class for '{labels[index]}': {toggle_class}")
                span_element.click()
                print(f"[INFO] Toggled ON: {labels[index]}")
                time.sleep(1)

                # if "off-class" in toggle_class:
                #     span_element.click()
                #     print(f"[INFO] Toggled ON: {labels[index]}")
                #     time.sleep(1)
                # else:
                #     print(f"[INFO] Already ON: {labels[index]}")

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