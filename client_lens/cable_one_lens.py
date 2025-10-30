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

class CableOneLens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def click_cableone_lens(self):
        try:
            cableone_lens = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(LensLocators.CABLE_LENS)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cableone_lens)
            time.sleep(1)
            try:
                cableone_lens.click()  # Try normal click
            except:
                self.driver.execute_script("arguments[0].click();", cableone_lens)  # JavaScript fallback
            print("[INFO] Cable lens clicked.")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to click cable  lens: {e}")
            return False

    # def verify_close_button_clickable(self):
    #     """Verify that the confirm button is clickable."""
    #     try:
    #         confirm_button = WebDriverWait(self.driver, 30).until(
    #             EC.element_to_be_clickable(LensLocators.CLOSE_BUTTON)
    #         )
    #         print("[INFO] Confirm button is clickable.Clicking now...")
    #         confirm_button.click()
    #         return True
    #     except Exception as e:
    #         print(f"[ERROR] Confirm button is not clickable: {e}")
    #         return False

    def verify_lens_title(self):
        """Verify that the lens title is 'Cell Towers' and return the result."""
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.CABLE_LENS_TITLE)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "Cable One":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Cable One', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_cableone_checkbox(self):
        """Verify that the cox checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.CABLE_LENS_CHECKBOX)
            )
            if checkbox.is_selected():
                print("[INFO] CABLE checkbox is checked.")
                return True
            else:
                print("[ERROR] CABLE checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] CABLE checkbox verification failed: {e}")
            return False


    def toggle_off_all_switches_and_assert(self):
        """Turn OFF all toggles and assert label + state."""

        try:
            time.sleep(10)

            for index, (by, toggle_xpath) in enumerate(LensLocators.CABLE_LENS_TOGGLE):
                # Click the toggle
                toggle_element = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((by, toggle_xpath))
                )
                toggle_element.click()
                label_text = CABLE_ONE_LABELS[index]
                print(f"[INFO] Clicked toggle {label_text}: {toggle_xpath}")

                label_xpath = f'//div[@class="color-legend-item"]//span[.="{label_text}"]'
                label_element = WebDriverWait(self.driver, 20).until(
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
            toggles = LensLocators.CABLE_LENS_TOGGLE
            labels = CABLE_ONE_LABELS

            for index, (by, span_locator) in enumerate(toggles):
                # Find the <span> to click
                span_element = WebDriverWait(self.driver, 20).until(
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



    def toggle_off_all_switches_and_assert_new_dev(self):
        """Turn OFF all toggles and assert label + state."""

        try:
            time.sleep(10)

            for index, (by, toggle_xpath) in enumerate(LensLocators.NEW_DEV_TOGGLE_CABLE_ONE):
                # Click the toggle
                toggle_element = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((by, toggle_xpath))
                )
                toggle_element.click()
                label_text = NEW_DEV_CABLE_ONE[index]
                print(f"[INFO] Clicked toggle {label_text}: {toggle_xpath}")

                label_xpath = f'//div[@class="color-legend-item"]//span[.="{label_text}"]'
                label_element = WebDriverWait(self.driver, 60).until(
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

    def toggle_on_all_switches_and_assert_new_dev(self):
        """
        Turn ON all  toggles and assert they are ON by checking the absence of 'off-class' in the input tag.
        """
        try:
            toggles = LensLocators.NEW_DEV_TOGGLE_CABLE_ONE
            labels = NEW_DEV_CABLE_ONE

            for index, (by, span_locator) in enumerate(toggles):
                # Find the <span> to click
                span_element = WebDriverWait(self.driver, 60).until(
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


    # def right_click_cable_lens(self):
    #     try:
    #
    #         lens = WebDriverWait(self.driver,20).until(
    #             EC.visibility_of_element_located(LensLocators.CABLE_LENS)
    #         )
    #
    #         actions = ActionChains(self.driver)
    #         actions.context_click(lens).perform()
    #         print(f'[INFO] : Right clicked successfully on lens')
    #         return True
    #
    #     except Exception as e:
    #         print('[ERROR] : FAILED TO RIGHT CLICK ON LENS')
    #         return False
    #
    #
    # def get_cable_one_aoi_list(self):
    #     try:
    #         county_list = WebDriverWait(self.driver,30).until(
    #             EC.presence_of_all_elements_located(LensLocators.CABLE_SEARCH_VCTI_AOI)
    #         )
    #
    #         list_county = [i.text.strip() for i in county_list if i.text.strip()]
    #         print(f"Total counties found : {len(list_county)}")
    #         print(f'Counties : {list_county[::]}')
    #         print()
    #
    #         # footer_message_elem = WebDriverWait(self.driver, 30).until(
    #         #     EC.visibility_of_element_located(LensLocators.SEARCH_COUNTY_FOTTER_MESSAGE)
    #         # )
    #         # footer_message = footer_message_elem.text.strip()
    #
    #         # print(f"FOOTER MESSAGE : {footer_message}")
    #         return True
    #
    #     except Exception as e:
    #         print('[ERROR] : FAILED TO GET AOI LIST')
    #         return False
    #
    # def cable_one_search_aoi(self):
    #     try:
    #         county = WebDriverWait(self.driver,30).until(
    #             EC.element_to_be_clickable(LensLocators.SEARCH_COUNTY)
    #         )
    #         county.click()
    #         print('[INFO] : CLICKED ON PROVIDER PLACEHOLDER')
    #         time.sleep(2)
    #
    #         county_value = WebDriverWait(self.driver,30).until(
    #             EC.element_to_be_clickable(LensLocators.CABLE_ONE_AOI_VALUE)
    #         )
    #         county_value.click()
    #         print(f'[INFO] : CLICKED ON PROVIDER VALUE - {CABLE_ONE_AOI}')
    #         time.sleep(15)
    #         return True
    #
    #     except Exception as e:
    #         print('[ERROR] : FAILED TO CLICK ON COUNTY')
    #         return False
    #
    #
    # def cable_one_network(self):
    #     try:
    #
    #         lens = WebDriverWait(self.driver, 20).until(
    #             EC.visibility_of_element_located(LensLocators.CABLE_LENS)
    #         )
    #
    #         actions = ActionChains(self.driver)
    #         actions.context_click(lens).perform()
    #         print(f'[INFO] : Right clicked successfully on lens')
    #         time.sleep(3)
    #         county = WebDriverWait(self.driver, 30).until(
    #             EC.element_to_be_clickable(LensLocators.SEARCH_COUNTY)
    #         )
    #         county.click()
    #         print('[INFO] : CLICKED ON PROVIDER PLACEHOLDER')
    #         time.sleep(2)
    #
    #         cableone_network_radio = WebDriverWait(self.driver, 30).until(
    #             EC.element_to_be_clickable(LensLocators.CABLE_ONE_NETWORKS_RADIO_BUTTON)
    #         )
    #         cableone_network_radio.click()
    #         print('[INFO] : CLICKED ON CABLE ONE NETWORK RADIO BUTTON')
    #         time.sleep(1)
    #
    #         network_list = WebDriverWait(self.driver, 30).until(
    #             EC.presence_of_all_elements_located(LensLocators.CABLE_ONE_NETWORKS)
    #         )
    #
    #         list_county = [i.text.strip() for i in network_list if i.text.strip()]
    #         print(f"Total counties found : {len(list_county)}")
    #         print(f'Counties : {list_county[::]}')
    #         print()
    #
    #         network_value = WebDriverWait(self.driver, 30).until(
    #             EC.element_to_be_clickable(LensLocators.CABLE_ONE_NETWORK)
    #         )
    #         network_value.click()
    #         print(f'[INFO] : CLICKED ON PROVIDER VALUE - {CABLE_ONE_NETWORK_VALUE}')
    #         time.sleep(15)
    #         return True
    #
    #     except Exception as e:
    #         print('[ERROR] : FAILED TO CLICK ON COUNTY')
    #         return False

