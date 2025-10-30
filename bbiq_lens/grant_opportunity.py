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

class GrantLens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def click_grant_lens(self):
        try:
            grant_lens = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(LensLocators.Grant_Opportunity_lens)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", grant_lens)
            time.sleep(1)
            try:
                grant_lens.click()  # Try normal click
            except:
                self.driver.execute_script("arguments[0].click();", grant_lens)  # JavaScript fallback
            print("[INFO] GRANT OPPORTUNITY Boundaries lens clicked.")
        except Exception as e:
            print(f"[ERROR] Failed to click GRANT OPPORTUNITY Boundaries lens: {e}")

    def verify_close_button_clickable(self):
        """Verify that the confirm button is clickable."""
        try:
            warning_text = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.WARNING_MESSAGE)
            )
            print(f'[INFO] : WARNING MESSAGE CAPTURED --> {warning_text.text}')
            confirm_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.Grant_close)
            )
            print("[INFO] Clicked on Confirm Button")
            confirm_button.click()
            return True
        except Exception as e:
            print(f"[ERROR] Confirm button is not clickable: {e}")
            return False

    def verify_lens_title(self):
        """Verify that the lens title is 'GRANT OPPORTUNITY  Boundaries' and return the result."""
        time.sleep(3)
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.Lens_title_GO)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "Grant Opportunity Rating":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Grant Opportunity Rating', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_grant_lens_checkbox(self):
        """Verify that the GRANT Boundaries checkbox is checked."""
        try:
            time.sleep(3)
            checkbox = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located(LensLocators.GO_legend_checkbox)
            )
            if checkbox.is_selected():
                print("[INFO] GRANT Boundaries checkbox is checked.")
                return True
            else:
                print("[ERROR] GRANT Boundaries checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] GRANT Boundaries checkbox verification failed: {e}")
            return False

    def grant_opportunity_opacity(self, offset):

        try:
            time.sleep(5)
            # **Wait for opacity button to be clickable**
            print("[INFO] Waiting for opacity button...")
            time.sleep(3)
            opacity_button3 = WebDriverWait(self.driver, 40).until(
                EC.element_to_be_clickable(LensLocators.Opacity_GO)
            )
            print("[INFO] Opacity button found, clicking...")
            opacity_button3.click()

            # **Ensure the slider is present & visible**
            print("[INFO] Waiting for opacity slider...")
            opacity_slider3 = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.Opacity_slider_GO)
            )
            print("[INFO] Opacity slider found.")

            # **Ensure slider is interactable before moving**
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(LensLocators.Opacity_slider_GO)
            )
            print("[INFO] Opacity slider is clickable.")

            # **Perform drag action**
            actions = ActionChains(self.driver)
            actions.move_to_element(opacity_slider3).click_and_hold().move_by_offset(offset, 0).release().perform()
            print(f"[INFO] Opacity adjusted by offset: {offset}")

            return True  # **Return success**

        except Exception as e:
            print(f"[ERROR] Failed to adjust opacity: {e}")
            return False

    def grant_opportunity_filter(self):
        """Filters for Grant opportunity lens."""
        wait = WebDriverWait(self.driver, 10)

        try:
            # Open filter
            filter_icon = wait.until(EC.presence_of_element_located(LensLocators.GRANT_OPPORTUNITY_FILTER))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", filter_icon)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", filter_icon)
            print("Filter icon clicked.")

            # Get sliders
            total_bsl_slider = wait.until(EC.presence_of_element_located(LensLocators.GRANT_TOTAL_BSL_SLIDER))
            growth_slider = wait.until(EC.presence_of_element_located(LensLocators.ELIGIBLE_BSL))
            actions = ActionChains(self.driver)

            def move_slider(slider, offset):
                actions.click_and_hold(slider).move_by_offset(offset, 0).release().perform()
                time.sleep(1)

            # Initial move (can be skipped or used as warm-up)
            move_slider(total_bsl_slider, 50)
            move_slider(growth_slider, 50)

            # Reset
            reset_btn = wait.until(EC.element_to_be_clickable(LensLocators.GRANT_RESET))
            reset_btn.click()
            print("Scenario 1: Reset action performed.")

            # Now set invalid values (Total BSL < Growth)
            move_slider(total_bsl_slider, 70)  # move by 50
            move_slider(growth_slider, 20)  # move by 70
            print("Scenario 2: Submit button disabled")

            try:
                error_element = wait.until(
                    EC.visibility_of_element_located()
                )
                if error_element.is_displayed():
                    print("Error Message Displayed: ", error_element.text)

                    # Check if submit button is disabled
                    submit_btn = self.driver.find_element
                    is_disabled = submit_btn.get_attribute("disabled")
                    if is_disabled:
                        print("Submit button is disabled due to validation error.")
                    else:
                        print("Submit button is NOT disabled when it should be.")

                    # Move total BSL further to fix
                    move_slider(total_bsl_slider, 90)
                    print("Scenario 3: Submit button enabled")
            except Exception:
                print("No validation message displayed.")

            submit_btn1 = wait.until(EC.element_to_be_clickable(LensLocators.GRANT_SUBMIT))
            submit_btn1.click()

            close_btn = wait.until(EC.element_to_be_clickable(LensLocators.GRANT_CLOSE))
            close_btn.click()

            return True

        except Exception as e:
            print(f"Error during grant opportunity filter setup: {e}")
            return False

    def toggle_off_all_switches_and_assert(self):
        """Turn OFF all toggles and assert label + state."""

        try:
            time.sleep(3)

            for index, (by, toggle_xpath) in enumerate(LensLocators.Grant_Opportunity_Lens_Toggle):
                # Click the toggle
                toggle_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((by, toggle_xpath))
                )
                toggle_element.click()
                label_text = GRANT_OPPORTUNITY_LABELS[index]
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
            toggles = LensLocators.Grant_Opportunity_Lens_Toggle
            labels = GRANT_OPPORTUNITY_LABELS

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

