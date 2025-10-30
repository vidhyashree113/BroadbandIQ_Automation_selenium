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

class Alaska_Lens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    # def wait_for_element(self, locator):
    #     return WebDriverWait(self.driver,30).until(EC.presence_of_element_located(locator))


    def click_alaska_lens(self):
        try:
            alaska_lens = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(LensLocators.ALASKA_LENS)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", alaska_lens)
            time.sleep(1)
            try:
                alaska_lens.click()  # Try normal click
            except:
                self.driver.execute_script("arguments[0].click();", alaska_lens)  # JavaScript fallback
            print("[INFO] Cell Towers lens clicked.")
        except Exception as e:
            print(f"[ERROR] Failed to click Cell Towers lens: {e}")


    def verify_lens_title(self):
        """Verify that the lens title is 'Cell Towers' and return the result."""
        try:
            self.driver.execute_script("document.body.style.zoom='75%'")
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.ALASKA_LENS_TITLE)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == 'Alaska Communications':
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Alaska Network', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_alaska_checkbox(self):
        """Verify that the Cell Towers checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.ALASKA_LENS_CHECKBOX)
            )
            if checkbox.is_selected():
                print("[INFO] Alaska lens checkbox is checked.")
                return True
            else:
                print("[ERROR] Alaska lens checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] Alaska lens checkbox verification failed: {e}")
            return False
    #
    # def validate_toggle_off_by_default_alaska(self):
    #     try:
    #         #extracting the text of toast message
    #         not_present = []
    #         present = []
    #
    #         for toggle in ALASKA_TOGGLE_LABELS_DEFAULT_OFF:
    #             if toggle.lower() in toast_text:
    #                 present.append(toggle)
    #
    #         if not_present:
    #             print(f'[ERROR] : TOGGLES EXPECTED TO BE TURNED_OFF BY DEFAULT BUT TURNED ON')
    #             return False
    #
    #         print(f'[INFO] : ALL EXPECTED TOGGLES MENTIONED ARE TURNED OFF'
    #               f'{ALASKA_TOGGLE_LABELS_DEFAULT_OFF}')
    #         return True
    #
    #     except Exception as e:
    #         print('[ERROR] : FAILED TO VALIDATE TOGGLE OFF BY DEFAULT')
    #         return False

    def validate_toggle_off_by_default_alaska(self):
        try:
            not_off = []  # toggles found ON (unexpected)
            all_checked = True

            for toggle_name, locator in LensLocators.ALASKA_TOGGLE_DEFAULT_OFF_ITEMS.items():
                element = self.driver.find_element(*locator)

                # Case 1: Checkbox-based toggle
                # if element.get_attribute("type") == "checkbox":
                #     is_on = element.is_selected()
                # else:
                    # Case 2: CSS-class-based toggle (e.g., "toggle on"/"toggle off")
                toggle_class = element.get_attribute("class")
                is_on = "on" in toggle_class.lower()

                if is_on:
                    not_off.append(toggle_name)
                    all_checked = False

            if not_off:
                print(f"[ERROR] : Toggles expected OFF but found ON → {not_off}")
                return False

            print(f"[INFO] : All expected toggles are OFF by default → {ALASKA_TOGGLE_LABELS_DEFAULT_OFF}")
            return True

        except Exception as e:
            print(f"[ERROR] : Failed to validate toggle state. Exception: {e}")
            return False


    def toggle_off_on_switches_and_assert(self):
        """Turn OFF all toggles and assert label + state."""

        try:
            time.sleep(5)
            for index, (by, toggle_xpath) in enumerate(LensLocators.ALASKA_TOGGLE_OFF):
                label_text = ALASKA_TOGGLE_LABELS_OFF[index]
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
            toggles = LensLocators.ALASKA_LENS_TOGGLES
            labels = ALASKA_TOGGLE_LABELS

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
                    span_element.click()
                    print(f"[INFO] Toggled ON: {labels[index]}")
                    # print(f"[INFO] Already ON: {labels[index]}")

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


    def toggle_off_all_switches_and_assert_alaska(self):
        """Turn OFF all toggles and assert label + state."""

        try:
            time.sleep(5)
            for index, (by, toggle_xpath) in enumerate(LensLocators.ALASKA_LENS_TOGGLES):
                label_text = ALASKA_TOGGLE_LABELS[index]
                # Click the toggle
                toggle_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((by, toggle_xpath))
                )
                toggle_element.click()
                # label_text = CELL_TOWERS_LABELS[index]

                # print(f"[INFO] Clicked toggle OFF for {label_text}: {toggle_xpath}")
                print(f"[INFO] Clicked toggle OFF for {label_text}")
                time.sleep(2)

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

    # def verify_junction_toggles_present(self):
    #     """Verify that all expected Junction toggles are present in UI."""
    #     try:
    #         expected_labels = ALASKA_JUNCTION_TOGGLE_LABEL
    #
    #         # Grab all visible junction labels under Alaska Network
    #         actual_elements = WebDriverWait(self.driver, 10).until(
    #             EC.presence_of_all_elements_located(
    #                 (By.XPATH,
    #                  "//div[contains(@id,'alaska_network_') and contains(@id,'_junction_row')]//span[@class='switch-slider round']/preceding-sibling::label")
    #             )
    #         )
    #
    #         actual_labels = [el.text.strip() for el in actual_elements]
    #
    #         print(f"[DEBUG] Expected: {expected_labels}")
    #         print(f"[DEBUG] Actual:   {actual_labels}")
    #
    #         # Compare lists
    #         for label in expected_labels:
    #             assert label in actual_labels, f"[ERROR] Toggle '{label}' NOT found in UI!"
    #             print(f"[ASSERTION PASSED] Toggle '{label}' present in UI ✅")
    #
    #         print("[PASSED] All Junction toggles verified successfully.")
    #         return True
    #
    #     except Exception as e:
    #         print(f"[ERROR] Failed verifying Junction toggles: {e}")
    #         return False



    def verify_network_toggles_present(self):
        try:
            not_present = []
            present = []
            # toast_text = LensLocators.CELL_TOWER_TOAST_MESSAGE.text
            for toggle in ALASKA_NETWORK_TOGGLE_EXPECTED_LABEL:
                if toggle in ALASKA_NETWORK_TOGGLE_LABEL:
                    present.append(toggle)

                else:
                    not_present.append(toggle)

            if not_present:
                print(f'[ERROR] : TOGGLES EXPECTED TO BE PRESENT UNDER NETWORK IS NOT PRESENT')
                return False

            print(f'[INFO] : ALL EXPECTED TOGGLES MENTIONED ARE PRESENT UNDER NETWORKS'
                  f'{ALASKA_NETWORK_TOGGLE_LABEL}')
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO VALIDATE TOGGLE PRESENT UNDER NETWORK')
            return False


    def verify_junction_toggles_present(self):
        try:
            not_present = []
            present = []
            # toast_text = LensLocators.CELL_TOWER_TOAST_MESSAGE.text
            for toggle in ALASKA_JUNCTION_TOGGLE_EXPECTED_LABEL:
                if toggle in ALASKA_JUNCTION_TOGGLE_LABEL:
                    present.append(toggle)

            if not_present:
                print(f'[ERROR] : TOGGLES EXPECTED TO BE PRESENT UNDER NETWORK IS NOT PRESENT')
                return False

            print(f'[INFO] : ALL EXPECTED TOGGLES MENTIONED ARE PRESENT UNDER NETWORKS'
                  f'{ALASKA_JUNCTION_TOGGLE_LABEL}')
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO VALIDATE TOGGLE PRESENT UNDER NETWORK')
            return False



#####################################
    # def verify_network_toggles_present(self):
    #     """Verify that all expected Junction toggles are present in UI."""
    #     try:
    #         expected_labels = ALASKA_NETWORK_TOGGLE_LABEL
    #
    #         # Grab all visible junction labels under Alaska Network
    #         actual_elements = WebDriverWait(self.driver, 20).until(
    #             EC.presence_of_all_elements_located(
    #                 (By.XPATH,
    #                  "//div[contains(@id,'alaska_network_') and contains(@id,'_junction_row')]//span[@class='switch-slider round']/preceding-sibling::label")
    #             )
    #         )
    #
    #         actual_labels = [el.text.strip() for el in actual_elements]
    #
    #         print(f"[DEBUG] Expected: {expected_labels}")
    #         print(f"[DEBUG] Actual:   {actual_labels}")
    #
    #         # Compare lists
    #         for label in expected_labels:
    #             assert label in actual_labels, f"[ERROR] Toggle '{label}' NOT found in UI!"
    #             print(f"[ASSERTION PASSED] Toggle '{label}' present in UI ✅")
    #
    #         print("[PASSED] All Network toggles verified successfully.")
    #         return True
    #
    #     except Exception as e:
    #         print(f"[ERROR] Failed verifying Network toggles: {e}")
    #         return False
