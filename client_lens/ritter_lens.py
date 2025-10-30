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

class RitterLens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def click_ritter_lens(self):
        try:
            ritter_lens = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.RITTER_LENS_ICON)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ritter_lens)
            time.sleep(1)
            try:
                ritter_lens.click()  # Try normal click
            except:
                self.driver.execute_script("arguments[0].click();", ritter_lens)  # JavaScript fallback
            print("[INFO] Ritter lens clicked.")
        except Exception as e:
            print(f"[ERROR] Failed to click Ritter lens: {e}")

    def verify_lens_title_national(self):
        """Verify that the lens title is 'Ritter lens' and return the result."""
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.LENS_TITLE_RI)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "Ritter":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Ritter', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_lens_title(self):
        """Verify that the lens title is 'Ritter lens' and return the result."""
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.LENS_TITLE_RI)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "Ritter":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Ritter', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_ritter_checkbox(self):
        """Verify that the Ritter checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.RI_LEGEND_CHECKBOX)
            )
            if checkbox.is_selected():
                print("[INFO] Ritter lens checkbox is checked.")
                return True
            else:
                print("[ERROR] Ritter lens checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] Ritter lens checkbox verification failed: {e}")
            return False

    def ritter_lens_opacity(self, offset):
        try:
            # **Wait for opacity button to be clickable**
            print("[INFO] Waiting for opacity button...")
            opacity_button1 = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.OPACITY_RI)
            )
            print("[INFO] Opacity button found, clicking...")
            opacity_button1.click()

            # **Ensure the slider is present & visible**
            print("[INFO] Waiting for opacity slider...")
            opacity_slider1 = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.OPACITY_SLIDER_RD)
            )
            print("[INFO] Opacity slider found.")

            # **Ensure slider is interactable before moving**
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(LensLocators.OPACITY_SLIDER_RD)
            )
            print("[INFO] Opacity slider is clickable.")

            # **Perform drag action**
            actions = ActionChains(self.driver)
            actions.move_to_element(opacity_slider1).click_and_hold().move_by_offset(offset, 0).release().perform()
            print(f"[INFO] Opacity adjusted by offset: {offset}")

            return True  # **Return success**

        except Exception as e:
            print(f"[ERROR] Failed to adjust opacity: {e}")
            return False

    # def toggle_off_all_switches_and_assert(self):
    #     """Turn OFF all Ritter lens toggles and assert label + state."""
    #
    #     try:
    #         time.sleep(3)
    #
    #         for index, (by, toggle_xpath) in enumerate(LensLocators.RITTER_LENS_TOGGLE):
    #             # Click the toggle
    #             toggle_element = WebDriverWait(self.driver, 10).until(
    #                 EC.element_to_be_clickable((by, toggle_xpath))
    #             )
    #             toggle_element.click()
    #             label_text = RITTER_LABELS[index]
    #             print(f"[INFO] Clicked toggle {label_text}: {toggle_xpath}")
    #             time.sleep(1)
    #
    #             # Get corresponding label
    #
    #             label_xpath = f"(//div[@class='color-legend-item']//span[normalize-space()='{label_text}'])[{1}]"
    #             label_element = self.driver.find_element(By.XPATH, label_xpath)
    #
    #             if not label_element.is_displayed():
    #                 print(f"[ERROR] Label not visible: '{label_text}'")
    #                 return False
    #             print(f"[INFO] Verified Actual and Expected Value : {label_text}")
    #
    #             # Check if the toggle is OFF
    #             input_xpath = toggle_xpath.replace("span[@class='switch-slider round']", "input[@type='checkbox']")
    #             input_element = self.driver.find_element(By.XPATH, input_xpath)
    #             toggle_class = input_element.get_attribute("class")
    #             # print(f"[DEBUG] Toggle class for '{label_text}': {toggle_class}")
    #
    #             if "off-class" not in toggle_class:
    #                 print(f"[ERROR] Toggle for '{label_text}' expected to be OFF, but it's ON!")
    #                 return False
    #
    #         print("[PASSED] All toggles OFF with correct labels verified.")
    #         return True
    #
    #     except Exception as e:
    #         print(f"[ERROR] Failed to toggle or verify switches: {e}")
    #         return False
    #
    # def toggle_on_all_switches_and_assert(self):
    #     """
    #     Turn ON all  toggles and assert they are ON by checking the absence of 'off-class' in the input tag.
    #     """
    #     try:
    #         toggles = LensLocators.RITTER_LENS_TOGGLE
    #         labels = RITTER_LABELS
    #
    #         for index, (by, span_locator) in enumerate(toggles):
    #             # Find the <span> to click
    #             span_element = WebDriverWait(self.driver, 10).until(
    #                 EC.presence_of_element_located((by, span_locator))
    #             )
    #             # self.driver.execute_script("arguments[0].scrollIntoView(true);", span_element)
    #
    #             input_element = span_element.find_element(By.XPATH, "./preceding-sibling::input")
    #             toggle_class = input_element.get_attribute("class")
    #             # print(f"[DEBUG] Initial INPUT class for '{labels[index]}': {toggle_class}")
    #
    #             if "off-class" in toggle_class:
    #                 span_element.click()
    #                 print(f"[INFO] Toggled ON: {labels[index]}")
    #                 time.sleep(1)
    #             else:
    #                 print(f"[INFO] Already ON: {labels[index]}")
    #
    #         for index, (by, span_locator) in enumerate(toggles):
    #             span_element = self.driver.find_element(by, span_locator)
    #             input_element = span_element.find_element(By.XPATH, "./preceding-sibling::input")
    #             toggle_class = input_element.get_attribute("class")
    #
    #             assert "off-class" not in toggle_class, f"[ERROR] {labels[index]} is still OFF!"
    #             print(f"[ASSERTION PASSED] {labels[index]} is ON ✅")
    #
    #         return True
    #
    #     except Exception as e:
    #         print(f"[ERROR] Failed to toggle ON all switches: {e}")
    #         return False


    def toggle_off_all_switches_and_assert(self):
        """Turn OFF all Ritter lens toggles and assert label + state."""

        try:
            time.sleep(3)

            for index, (by, toggle_xpath) in enumerate(LensLocators.RITTER_LENS_TOGGLE):
                # Click the toggle
                toggle_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((by, toggle_xpath))
                )
                toggle_element.click()
                label_text = RITTER_LABELS[index]
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
            toggles = LensLocators.RITTER_LENS_TOGGLE
            labels = RITTER_LABELS

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


    def capturing_warning_toast_message(self):
        try:
            toast_element = self.wait_for_element(LensLocators.RITTER_LENS_TOAST_MESSAGE)
            toast_text = toast_element.text.lower()
            # extracting the text of toast message
            not_present = []
            present = []
            print(f'[INFO] : CONFIRMATION MESSAGE - {toast_element.text}')
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO CAPTURE WARNING MESSAGE')
            return False

    def click_ritter_lens_county(self):
        try:
            ritter_lens = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.RITTER_LENS_ICON)
            )
            # print("DEBUG locator:", LensLocators.COVERAGE_AREA_LENS)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ritter_lens)
            time.sleep(1)

            actions = ActionChains(self.driver)
            actions.context_click(ritter_lens).perform()

            print("[INFO] Right-clicked on Ritter Lens.")


            #selecting county
            county = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.RITTER_LENS_COUNTY)
            )
            county.click()
            print('[INFO] : CLICKED ON PROVIDER PLACEHOLDER')
            time.sleep(2)

            county_value = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.RITTER_LENS_COUNTY_VALUE)
            )
            county_value.click()
            print(f'[INFO] : CLICKED ON PROVIDER VALUE - {RITTER_LENS_COUNTY_VALUE}')
            time.sleep(2)
            return True

        except Exception as e:
            print(f"[ERROR] Failed to click Ritter lens: {e}")
            return False


