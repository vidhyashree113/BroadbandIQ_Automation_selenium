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

class SkywireLens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def click_skywire_lens(self):
        try:
            skywire_lens = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(LensLocators.SKYWIRE_LENS)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", skywire_lens)
            time.sleep(1)
            try:
                skywire_lens.click()  # Try normal click
            except:
                self.driver.execute_script("arguments[0].click();", skywire_lens)  # JavaScript fallback
            print("[INFO] Skywire lens clicked.")
        except Exception as e:
            print(f"[ERROR] Failed to click skywire lens: {e}")

    def verify_close_button_clickable(self):
        """Verify that the confirm button is clickable."""
        try:
            confirm_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.CLOSE_BUTTON)
            )
            print("[INFO] Confirm button is clickable.Clicking now...")
            confirm_button.click()
            return True
        except Exception as e:
            print(f"[ERROR] Confirm button is not clickable: {e}")
            return False

    def verify_lens_title(self):
        """Verify that the lens title is 'Cell Towers' and return the result."""
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.SKYWIRE_LENS_TITLE)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "Skywire":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Skywire Networks', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_skywire_checkbox(self):
        """Verify that the skywire checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.SKYWIRE_LENS_CHECKBOX)
            )
            if checkbox.is_selected():
                print("[INFO] Skywire checkbox is checked.")
                return True
            else:
                print("[ERROR] Skywire checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] Skywire checkbox verification failed: {e}")
            return False

    def verify_los_filter(self):
        """Verify that the los filter is clicked"""
        try:
            time.sleep(5)
            filter_button = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.SKYWIRE_LOS_FILTER)
            )
            filter_button.click()
            print("[INFO] Skywire LOS filter is clicked.")

            # slider button sliding

            slider = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.SKYWIRE_SLIDER)
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", slider)
            time.sleep(1)

            # Drag the slider (you can adjust the offset based on expected value)
            actions = ActionChains(self.driver)
            actions.click_and_hold(slider).move_by_offset(80, 0).release().perform()
            print("[INFO] Slider adjusted.")
            time.sleep(3)
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(LensLocators.SKYWIRE_LOS_SUBMIT))
            # print("[DEBUG] Clicking Submit button")
            submit_button.click()
            # print("[DEBUG] Submit clicked. Waiting for result...")
            print("[INFO] LOS Submit button clicked.")
            return True

        except Exception as e:
            print(f"Error in LOS filter workflow: {e}")
            return False

            #
            # # Dragging the slider
            # actions = ActionChains(self.driver)
            # actions.click_and_hold(slider).move_by_offset(50, 0).release().perform()
            # time.sleep(2)
            # print("[INFO] Skywire LOS filter slider is slided.")

            # Step 3: Click the visible action button (submit/reset/cancel)
            # for locator in [LensLocators.SKYWIRE_LOS_SUBMIT, LensLocators.SKYWIRE_LOS_RESET,
            #                 LensLocators.SKYWIRE_LOS_CLOSE]:

    def toggle_off_all_switches_and_assert(self):
        """Turn OFF all toggles and assert label + state."""

        try:
            time.sleep(5)

            for index, (by, toggle_xpath) in enumerate(LensLocators.SKYWIRE_TOGGLE):
                # Click the toggle
                toggle_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((by, toggle_xpath))
                )
                toggle_element.click()
                label_text = SKYWIRE_LENS_LABLES[index]
                print(f"[INFO] Clicked toggle {label_text}: {toggle_xpath}")

                label_xpath = f"//div[@class='color-legend-item']//span[normalize-space()='{label_text}']"
                label_element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, label_xpath))
                )

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
            toggles = LensLocators.SKYWIRE_TOGGLE
            labels = SKYWIRE_LENS_LABLES

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