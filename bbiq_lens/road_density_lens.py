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

class RoadDensityLens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def click_road_density_lens(self):
        try:
            road_density_lens = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.ROAD_DENSITY_LENS_ICON)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", road_density_lens)
            time.sleep(1)
            try:
                road_density_lens.click()  # Try normal click
            except:
                self.driver.execute_script("arguments[0].click();", road_density_lens)  # JavaScript fallback
            print("[INFO] Road Density lens clicked.")
        except Exception as e:
            print(f"[ERROR] Failed to click Road Density lens: {e}")

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

    def verify_lens_title_national(self):
        """Verify that the lens title is 'Density Locations per road mile' and return the result."""
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.LENS_TITLE_RD)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "Density Locations per road mile":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Density Locations per road mile', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_lens_title(self):
        """Verify that the lens title is 'Density Locations per road mile' and return the result."""
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.LENS_TITLE_RD)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "Density Locations per road mile":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Density Locations per road mile', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_road_density_checkbox(self):
        """Verify that the Competitive Opportunity checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(LensLocators.RD_LEGEND_CHECKBOX)
            )
            if checkbox.is_selected():
                print("[INFO] Road Density checkbox is checked.")
                return True
            else:
                print("[ERROR] Road Density checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] Road Density checkbox verification failed: {e}")
            return False

    def road_density_opacity(self, offset):
        try:
            # **Wait for opacity button to be clickable**
            print("[INFO] Waiting for opacity button...")
            opacity_button1 = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.OPACITY_RD)
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

    # def randomly_toggle_two_switches(self):
    #     """Randomly turn OFF any 2 toggles while keeping others ON."""
    #     try:
    #         toggles_to_turn_off = random.sample(LensLocators.ROAD_DENSITY_TOGGLE, 2)
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
    # def randomly_toggle_two_switches(self):
    #     """Randomly turn OFF any 2 toggles and assert their state changed correctly."""
    #     try:
    #         toggles_to_click = random.sample(LensLocators.ROAD_DENSITY_TOGGLE, 2)
    #         print(f"[INFO] Selected toggles to turn off: {toggles_to_click}")
    #
    #         for span_by, span_locator in toggles_to_click:
    #
    #             span_element = WebDriverWait(self.driver, 10).until(
    #                 EC.element_to_be_clickable((span_by, span_locator))
    #             )
    #
    #             span_element.click()
    #             print(f"[INFO] Clicked toggle span: {span_locator}")
    #
    #             input_locator = span_locator.replace("span[@class='switch-slider round']", "input[@type='checkbox']")
    #             input_element = self.driver.find_element(By.XPATH, input_locator)
    #             toggle_class = input_element.get_attribute("class")
    #             print(f"[DEBUG] Toggle input class after click: {toggle_class}")
    #
    #             if "off-class" not in toggle_class:
    #                 print(f"[ERROR] Toggle {input_locator} expected to be OFF, but it's ON!")
    #                 return False
    #
    #         print("[PASSED] 2 toggles turned OFF and verified.")
    #         return True
    #
    #     except Exception as e:
    #         print(f"[ERROR] Failed to toggle switches: {e}")
    #         return False

    def toggle_off_all_switches_and_assert(self):
        """Turn OFF all Community Anchor toggles and assert label + state."""

        try:
            time.sleep(3)

            for index, (by, toggle_xpath) in enumerate(LensLocators.ROAD_DENSITY_TOGGLE):
                # Click the toggle
                toggle_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((by, toggle_xpath))
                )
                toggle_element.click()
                label_text = ROAD_DENSITY_LABELS[index]
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
            toggles = LensLocators.ROAD_DENSITY_TOGGLE
            labels = ROAD_DENSITY_LABELS

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


