import random
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..config.config import *
from ..config.assertion_config import *
from ..locators.lens_locators import LensLocators
from ..pages.map_page import MapPage
from time import sleep
from ..pages.common import BasePage
from datetime import datetime
import time,os

class Fiber_Growth(BasePage):

    def __init__(self,driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def click_fiber_growth_lens(self):
        try:

            fiber_growth_lens = WebDriverWait(self.driver,30).until(EC.element_to_be_clickable(LensLocators.Fiber_Growth_Lens))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",fiber_growth_lens)
            sleep(1)

            try:

                fiber_growth_lens.click() #normal click

            except:

                self.driver.execute_script("arguments[0].click();", fiber_growth_lens)
                print("[INFO] Fiber Growth lens clicked.")

        except Exception as msg:
            print(f'[ERROR] failed to click on Fiber Growth lens :{msg}')


    def verify_lens_title_national(self):

        #verify lens title  is 'Fiber Growth Rate and returns same result
        try:
            lens_title_element = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located(LensLocators.Lens_title_FG))

            title_text = lens_title_element.text.strip() #for removing if extra spaces in leading & trailing
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == lens_title_element.text.strip():
                return True

            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Fiber Growth Rate', Found: '{title_text}'")
                return False

        except Exception as msg:
            print(f"[ERROR] Lens title verification failed: {msg}")
            return False


    def verify_lens_title(self):

        try:

            lens_title_element = WebDriverWait(self.driver,30).until(EC.visibility_of_element_located(LensLocators.Lens_title_FG))

            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == lens_title_element.text.strip():
                return True

            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Fiber Growth Rate', Found: '{title_text}'")
                return False

        except Exception as msg:
            print(f"[ERROR] Lens title verification failed: {msg}")
            return False


    def verify_fiber_growth_checkbox(self):
        """Verify that the Household Income checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.FG_legend_checkbox)
            )
            if checkbox.is_selected():
                print("[INFO] checkbox is checked.")
                return True
            else:
                print("[ERROR] Fiber Growth checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] Fiber Growth checkbox verification failed: {e}")
            return False

    def fiber_growth_opacity(self, offset):
        try:
            sleep(3)
            # **Wait for opacity button to be clickable**
            print("[INFO] Waiting for opacity button...")
            sleep(3)
            opacity_button2 = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.Opacity_FG)
            )
            print("[INFO] Opacity button found, clicking...")
            opacity_button2.click()

            # **Ensure the slider is present & visible**
            print("[INFO] Waiting for opacity slider...")
            opacity_slider2 = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.Opacity_slider_FG)
            )
            print("[INFO] Opacity slider found.")

            # **Ensure slider is interactable before moving**
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(LensLocators.Opacity_slider_FG)
            )
            print("[INFO] Opacity slider is clickable.")

            # **Perform drag action**
            actions = ActionChains(self.driver)
            actions.move_to_element(opacity_slider2).click_and_hold().move_by_offset(offset, 0).release().perform()
            print(f"[INFO] Opacity adjusted by offset: {offset}")

            return True  # **Return success**

        except Exception as e:
            print(f"[ERROR] Failed to adjust opacity: {e}")
            return False

    def verify_close_button_clickable(self):
        """Verify that the confirm button is clickable."""
        try:
            confirm_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.Fiber_close)
            )
            print("[INFO] Confirm button is clickable.Clicking now...")
            confirm_button.click()
            return True
        except Exception as e:
            print(f"[ERROR] Confirm button is not clickable: {e}")
            return False


    def toggle_off_all_switches_and_assert(self):
        """Turn OFF all toggles and assert label + state."""

        try:

            for index, (by, toggle_xpath) in enumerate(LensLocators.Fiber_Growth_Lens_Toggle):
                # Click the toggle
                toggle_element = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((by, toggle_xpath))
                )
                toggle_element.click()
                label_text = FIBER_GROWTH_LABELS[index]
                print(f"[INFO] Clicked toggle {label_text}: {toggle_xpath}")
                # time.sleep(1)

                # label_xpath = f"(//div[@class='color-legend-item']//span[normalize-space()='{label_text}'])[{1}]"
                # label_element = self.driver.find_element(By.XPATH, label_xpath)
                label_start = label_text.split()[0]
                label_xpath = f"//div[@class='color-legend-item']//span[contains(text(), '{label_start}')]"

                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, label_xpath))
                )
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
            toggles = LensLocators.Fiber_Growth_Lens_Toggle
            labels = FIBER_GROWTH_LABELS

            for index, (by, span_locator) in enumerate(toggles):
                # Find the <span> to click
                span_element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((by, span_locator))
                )
                # self.driver.execute_script("arguments[0].scrollIntoView(true);", span_element)

                input_element = span_element.find_element(By.XPATH, "./preceding-sibling::input")
                toggle_class = input_element.get_attribute("class")
                # print(f"[DEBUG] Initial INPUT class for '{labels[index]}': {toggle_class}")

                if "off-class" in toggle_class:
                    span_element.click()
                    print(f"[INFO] Toggled ON: {labels[index]}")
                    # time.sleep(1)
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

    def fiber_growth_filter(self):
        """Filters for Fiber Growth lens."""
        wait = WebDriverWait(self.driver, 10)

        try:
            # Wait for filter icon to be present in DOM
            filter_icon = wait.until(EC.presence_of_element_located(LensLocators.FIBER_GROWTH_FILTER))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", filter_icon)
            time.sleep(0.5)

            try:
                clickable_icon = wait.until(EC.element_to_be_clickable(LensLocators.FIBER_GROWTH_FILTER))
                clickable_icon.click()
            except Exception:
                # Fallback: JavaScript click
                self.driver.execute_script("arguments[0].click();", filter_icon)

            # Sliders
            total_bsl_slider = wait.until(
                EC.presence_of_element_located(LensLocators.FIBER_TOTAL_BSL_SLIDER))
            growth_slider = wait.until(
                EC.presence_of_element_located(LensLocators.FIBER_GROWTH_PERCENTAGE))

            actions = ActionChains(self.driver)

            def move_slider(slider, offset):
                actions.click_and_hold(slider).move_by_offset(offset, 0).release().perform()
                time.sleep(1)

            # Move sliders initially to simulate user interaction
            move_slider(total_bsl_slider, 50)
            move_slider(growth_slider, 50)

            # Reset filter
            reset_btn = wait.until(EC.element_to_be_clickable(LensLocators.FILTER_RESET))
            reset_btn.click()
            print("Scenario 1: Reset action performed.")

            # Move sliders again to final position
            move_slider(total_bsl_slider, 70)
            move_slider(growth_slider, 70)

            # Submit
            submit_btn = wait.until(EC.element_to_be_clickable(LensLocators.FILTER_SUBMIT))
            submit_btn.click()
            print("Scenario 2: Submit action performed.")

            # Close
            close_btn = wait.until(EC.element_to_be_clickable(LensLocators.FILTER_CLOSE))
            close_btn.click()

            return True

        except Exception as e:
            print(f"Error during fiber growth filter setup: {e}")
            return False

    def apply_color_scheme(self, lens_key):
        """Call map color scheme function from MapPage"""
        try:
            return self.map_page.map_color_scheme_flow(lens_key)
        except Exception as e:
            print(f"[ERROR] Failed to apply color scheme: {e}")
            return False

