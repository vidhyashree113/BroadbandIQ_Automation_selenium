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


class CellTowersLens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def wait_for_element(self, locator):
        return WebDriverWait(self.driver,30).until(EC.presence_of_element_located(locator))

    def click_cell_towers_lens(self):
        try:
            cell_towers_lens = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(LensLocators.TOWERS_LENS_ICON)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cell_towers_lens)
            time.sleep(1)
            try:
                cell_towers_lens.click()  # Try normal click
            except:
                self.driver.execute_script("arguments[0].click();", cell_towers_lens)  # JavaScript fallback
            print("[INFO] Cell Towers lens clicked.")
        except Exception as e:
            print(f"[ERROR] Failed to click Cell Towers lens: {e}")

    def verify_close_button_clickable(self):
        """Verify that the confirm button is clickable."""
        try:
            warning_text =  WebDriverWait(self.driver,30).until(
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
        """Verify that the lens title is 'Cell Towers' and return the result."""
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.LENS_TITLE_CT)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "Cell Towers":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Cell Towers', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_cell_towers_checkbox(self):
        """Verify that the Cell Towers checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.CT_LEGEND_CHECKBOX)
            )
            if checkbox.is_selected():
                print("[INFO] Cell Towers checkbox is checked.")
                return True
            else:
                print("[ERROR] Cell Towers checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] Cell Towers checkbox verification failed: {e}")
            return False

    def validate_toggle_off_by_default_campbell(self):
        try:
            toast_element = self.wait_for_element(LensLocators.CELL_TOWER_TOAST_MESSAGE)
            toast_text = toast_element.text.lower()
            # extracting the text of toast message
            not_present = []
            present = []
            print(f'[INFO] : CONFIRMATION MESSAGE - {toast_element.text}')
            # toast_text = LensLocators.CELL_TOWER_TOAST_MESSAGE.text
            for toggle in CELL_TOWERS_LABELS_DEFAULT_OFF_CAMPBELL:
                if toggle.lower() in toast_text:
                    present.append(toggle)

            if not_present:
                print(f'[ERROR] : TOGGLES EXPECTED TO BE TURNED_OFF BY DEFAULT BUT TURNED ON')
                return False

            print(f'[INFO] : ALL EXPECTED TOGGLES MENTIONED ARE TURNED OFF'
                  f'{CELL_TOWERS_LABELS_DEFAULT_OFF_CAMPBELL}')
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO VALIDATE TOGGLE OFF BY DEFAULT')
            return False

    def toggle_off_all_switches_and_assert(self):
        """Turn OFF all toggles and assert label + state."""

        try:
            time.sleep(5)
            for index, (by, toggle_xpath) in enumerate(LensLocators.CELL_TOWERS_LENS_TOGGLE):
                label_text = CELL_TOWERS_LABELS[index]
                # Click the toggle
                toggle_element = WebDriverWait(self.driver, 10).until(
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

    def toggle_on_all_switches_and_assert(self):
        """
        Turn ON all  toggles and assert they are ON by checking the absence of 'off-class' in the input tag.
        """
        try:
            time.sleep(5)
            toggles = LensLocators.CELL_TOWERS_LENS_TOGGLE
            labels = CELL_TOWERS_LABELS

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

    def toggle_off_all_switches_and_assert_campbell(self):
        """Turn OFF all toggles and assert label + state."""

        try:
            time.sleep(5)
            for index, (by, toggle_xpath) in enumerate(LensLocators.CELL_TOWERS_LENS_TOGGLE_CAMPBELL):
                label_text = CELL_TOWERS_LABELS_CAMPBELL[index]
                # Click the toggle
                toggle_element = WebDriverWait(self.driver, 10).until(
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

    def toggle_on_all_switches_and_assert_campbell(self):
        """
        Turn ON all  toggles and assert they are ON by checking the absence of 'off-class' in the input tag.
        """
        try:
            time.sleep(5)
            toggles = LensLocators.CELL_TOWERS_LENS_TOGGLE_CAMPBELL
            labels = CELL_TOWERS_LABELS_CAMPBELL

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





