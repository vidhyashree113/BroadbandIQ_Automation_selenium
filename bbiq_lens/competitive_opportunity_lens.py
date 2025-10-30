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

class CompetitiveOpportunityLens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def click_competitive_lens(self):
        try:
            competitive_lens = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(LensLocators.COMPETITIVE_LENS_ICON)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", competitive_lens)
            time.sleep(1)
            try:
                competitive_lens.click()  # Try normal click
            except:
                self.driver.execute_script("arguments[0].click();", competitive_lens)  # JavaScript fallback
            print("[INFO] Competitive Opportunity lens clicked.")
        except Exception as e:
            print(f"[ERROR] Failed to click Competitive Opportunity lens: {e}")

    # def click_competitive_lens(self):
    #     try:
    #         competitive_lens = WebDriverWait(self.driver, 60).until(
    #             EC.element_to_be_clickable(LensLocators.COMPETITIVE_LENS_ICON)
    #         )
    #         # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", competitive_lens)
    #
    #         time.sleep(1)
    #         try:
    #             competitive_lens.click()  # Try normal click
    #         except:
    #             self.driver.execute_script("arguments[0].click();", competitive_lens)  # JavaScript fallback
    #         print("[INFO] Competitive Opportunity lens clicked.")
    #     except Exception as e:
    #         print(f"[ERROR] Failed to click Competitive Opportunity lens: {e}")

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

    # def verify_lens_title(self):
    #     """Verify that the lens title is 'Opportunity Analysis'."""
    #     try:
    #         lens_title = WebDriverWait(self.driver, 30).until(
    #             EC.visibility_of_element_located(LensLocators.LENS_TITLE)
    #         )
    #         # assert lens_title.text == "Opportunity Analysis", "[ERROR] Lens title mismatch!"
    #         print("[INFO] Lens title is correctly displayed as 'Opportunity Analysis'.")
    #     except Exception as e:
    #         print(f"[ERROR] Lens title verification failed: {e}")
    def verify_lens_title(self):
        """Verify that the lens title is 'Opportunity Analysis' and return the result."""
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.LENS_TITLE)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "Opportunity Analysis":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Opportunity Analysis', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_competitive_checkbox(self):
        """Verify that the Competitive Opportunity checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.COMPETITIVE_LEGEND_CHECKBOX)
            )
            if checkbox.is_selected():
                print("[INFO] Competitive Opportunity checkbox is checked.")
                return True
            else:
                print("[ERROR] Competitive Opportunity checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] Competitive Opportunity checkbox verification failed: {e}")
            return False

    def competitive_opacity(self, value):
        try:
            print("[INFO] Waiting for opacity button...")
            opacity_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.OPACITY_CO)
            )
            print("[INFO] Opacity button found, clicking...")
            opacity_button.click()

            print("[INFO] Waiting for opacity slider...")
            slider = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.OPACITY_SLIDER_CO)
            )
            print("[INFO] Slider input element found.")

            # Set slider value directly using JavaScript
            self.driver.execute_script("""
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input'));
                arguments[0].dispatchEvent(new Event('change'));
            """, slider, str(value))

            print(f"[INFO] Slider value set to {value}")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to set opacity: {e}")
            return False

    # def randomly_toggle_two_switches(self):
    #     """Randomly turn OFF any 2 toggles while keeping others ON."""
    #     try:
    #         toggles_to_turn_off = random.sample(LensLocators.COMPETITIVE_TOGGLE, 2)
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
        """Turn OFF all toggles and assert label + state."""

        try:
            time.sleep(3)

            for index, (by, toggle_xpath) in enumerate(LensLocators.COMPETITIVE_TOGGLE):
                # Click the toggle
                toggle_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((by, toggle_xpath))
                )
                toggle_element.click()
                label_text = OPPORTUNITY_ANALYSIS_LABELS[index]
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
            toggles = LensLocators.COMPETITIVE_TOGGLE
            labels = OPPORTUNITY_ANALYSIS_LABELS

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



    def run_tc_001(self):
        """TC-001: Verify Confirm Button Clickable"""
        print("\n--- Running TC-001: Verify Confirm Button Clickable ---")

        map_page = MapPage(self.driver)

        map_page.search_county(COUNTY_NAME)
        time.sleep(5)

        map_page.click_icon()
        time.sleep(2)

        self.click_competitive_lens()
        time.sleep(3)

        if self.verify_close_button_clickable():
            print("[PASSED] TC-001: 'PASS' Confirm button is clickable.")
        else:
            print("[FAILED] TC-001: Confirm button is not clickable.")

        time.sleep(5)

    def run_tc_002(self):
        """TC-002: Verify Lens Title"""
        print("\n--- Running TC-002: Verify Lens Title ---")

        map_page = MapPage(self.driver)

        map_page.search_county(COUNTY_NAME)
        time.sleep(5)

        map_page.double_click_the_county()
        time.sleep(5)

        map_page.click_icon()
        time.sleep(2)

        self.click_competitive_lens()
        time.sleep(3)

        self.verify_lens_title()
        time.sleep(5)

    def run_tc_003(self):
        """TC-003: Verify Competitive Checkbox"""
        print("\n--- Running TC-003: Verify Competitive Checkbox ---")

        map_page = MapPage(self.driver)

        map_page.search_county(COUNTY_NAME)
        time.sleep(5)

        map_page.double_click_the_county()
        time.sleep(2)

        map_page.click_icon()
        time.sleep(2)

        self.click_competitive_lens()
        time.sleep(3)

        self.verify_competitive_checkbox()
        time.sleep(5)

    def run_tc_004(self):
        """TC-004: Adjust Opacity for Competitive Opportunity Layer"""
        print("\n--- Running TC-004: Adjust Opacity for Competitive Opportunity Layer ---")

        map_page = MapPage(self.driver)

        try:
            # Step 1: Search for County
            map_page.search_county(COUNTY_NAME)
            time.sleep(5)

            # Step 2: Double-click on County
            map_page.double_click_the_county()
            time.sleep(5)

            # Step 3: Click Chevron Icon
            map_page.click_icon()
            time.sleep(2)

            # Step 4: Click Competitive Opportunity Lens
            self.click_competitive_lens()
            time.sleep(3)

            # Step 5: Click Opacity and Adjust Slider
            self.competitive_opacity(offset=50)
            print("[PASSED] TC-004: Opacity adjustment successful.")

        except Exception as e:
            print(f"[FAILED] TC-004: Error encountered - {e}")

        time.sleep(5)

    def run_tc_005(self):
        """TC-005: Randomly Toggle Competitive Lens Options"""
        print("\n--- Running TC-005: Randomly Toggle Competitive Lens Options ---")

        map_page = MapPage(self.driver)

        map_page.search_county(COUNTY_NAME)
        time.sleep(5)
        map_page.double_click_the_county()
        time.sleep(2)
        map_page.click_icon()
        time.sleep(2)
        self.click_competitive_lens()
        time.sleep(3)

        self.randomly_toggle_two_switches()
        print("[PASSED] TC-005: Random toggling successful.")

        time.sleep(5)

    def run_tests(self):
        """Run all test cases"""
        map_page = MapPage(self.driver)

        self.run_tc_001()
        map_page.reset()
        self.run_tc_002()
        map_page.reset()
        self.run_tc_003()
        map_page.reset()
        self.run_tc_004()
        map_page.reset()
        self.run_tc_005()
        map_page.reset()


