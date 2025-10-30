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
# import time

class HotwireLens(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def click_hotwire_lens(self):
        try:
            hotwire_lens = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(LensLocators.HOTWIRE_LENS)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", hotwire_lens)
            time.sleep(1)
            try:
                hotwire_lens.click()  # Try normal click
            except:
                self.driver.execute_script("arguments[0].click();", hotwire_lens)  # JavaScript fallback
            print("[INFO] HotWire Lens clicked.")
        except Exception as e:
            print(f"[ERROR] Failed to click HotWire lens: {e}")

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
            print("[INFO] : Clicked on Confirm button...")
            confirm_button.click()
            return True
        except Exception as e:
            print(f"[ERROR] Confirm button is not clickable: {e}")
            return False

    def verify_lens_title(self):
        """Verify that the lens title is 'Area Boundaries' and return the result."""
        try:
            lens_title_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.HOTWIRE_LENS_TITLE)
            )
            title_text = lens_title_element.text.strip()
            print(f"[INFO] Lens title found: '{title_text}'")

            if title_text == "Hotwire":
                return True  #
            else:
                print(f"[ERROR] Lens title mismatch! Expected: 'Hotwire', Found: '{title_text}'")
                return False  #

        except Exception as e:
            print(f"[ERROR] Lens title verification failed: {e}")
            return False  #

    def verify_hotwire_checkbox(self):
        """Verify that the Area Boundaries checkbox is checked."""
        try:
            checkbox = WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located(LensLocators.HOTWIRE_LENS_CHECKBOX)
            )
            if checkbox.is_selected():
                print("[INFO] HOTWIRE LENS checkbox is checked.")
                return True
            else:
                print("[ERROR] HOTWIRE LENS checkbox is not checked!")
                return False
        except Exception as e:
            print(f"[ERROR] HOTWIRE LENS checkbox verification failed: {e}")
            return False


    def toggle_on_all_except_network(self):
        """Toggle ON all layers except municipal and city which are already ON by default."""
        try:
            time.sleep(2)
            for index, (by, toggle_xpath) in enumerate(LensLocators.HOTWIRE_LENS_TOGGLE_DEFAULT_OFF):  # only for specific 4
                input_element = self.driver.find_element(by, toggle_xpath)

                # Check if not checked initially
                if not input_element.get_attribute("checked"):
                    toggle_element = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((by, toggle_xpath.replace("input", "span")))
                    )
                    toggle_element.click()
                    print(f"[INFO] Toggled ON: {HOTWIRE_TOGGLE_DEFAULT_OFF[index]}")

            print("[PASSED] All required toggles are turned ON.")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to toggle ON HOA/CABINET toggles: {e}")
            return False


    def toggle_off_all_switches_and_assert(self):
        """Turn OFF all toggles, regardless of initial checked state or class."""

        try:
            time.sleep(5)
            for index, (by, toggle_xpath) in enumerate(LensLocators.HOTWIRE_TOGGLES):
                label_text = HOTWIRE_TOGGLE_LABELS[index]
                # Click the toggle
                toggle_element = WebDriverWait(self.driver, 20).until(
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


    def toggle_on_cabinet_toggle(self):
        try:
            time.sleep(2)
            for index, (by, toggle_xpath) in enumerate(LensLocators.HOT_WIRE_CABINET):  # only for specific 4
                input_element = self.driver.find_element(by, toggle_xpath)

                # Check if not checked initially
                if not input_element.get_attribute("checked"):
                    toggle_element = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((by, toggle_xpath.replace("input", "span")))
                    )
                    toggle_element.click()
                    print(f"[INFO] Toggled ON: {HOT_WIRE_CABINET_LABEL[index]}")

            print("[PASSED] Cabinets toggles are turned ON.")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to toggle ON CABINET toggles: {e}")
            return False


    def right_click_and_sales_opportunity(self):
        try:
            print("[INFO]: Right-clicked on the red-colored area (estimated position).")

            # old code
            canvas = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "mapboxgl-canvas"))
            )
            width = canvas.size['width']
            height = canvas.size['height']
            center_x = width // 2
            center_y = height // 2

            offset_x = center_x
            offset_y = center_y
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, center_x, center_y).click_and_hold(canvas).perform()
            print("[INFO]: right click happend...")

            # selecting ISP footprint
            # Hover and click "ISP Footprint Report"
            sales_opportunity = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.HOTWIRE_LENS_SALES_OPPORTUNITY)
            )
            # actions.move_to_element(sales_opportunity).click_and_hold().perform()
            # time.sleep(2)
            sales_opportunity1 = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(LensLocators.HOTWIRE_LENS_SALES_OPPORTUNITY)
            )
            sales_opportunity1.click()
            print('[INFO] : CLICKED ON SALES OPPORTUNITY')

            # commented code
            # state = WebDriverWait(self.driver, 30).until(
            #     EC.visibility_of_element_located((By.XPATH, "//a[contains(.,'Export Report')]//a[.='Export as PDF']"))
            # )
            # actions.move_to_element(state).click().perform()
            # print('[INFO]: Export PDF clicked')
            # time.sleep(2)
            #
            # # Enter description
            # textarea = WebDriverWait(self.driver, 30).until(
            #     EC.visibility_of_element_located((By.ID, "report-description"))
            # )
            # textarea.send_keys("Export report Erate PDF")
            #
            # time.sleep(2)
            #
            # # Click submit
            # submit_btn = WebDriverWait(self.driver, 30).until(
            #     EC.element_to_be_clickable((By.ID, "add_report_submit_btn"))
            # )
            # submit_btn.click()

            print("[INFO]: Clicked on Sales Opportunity successfully.")
            return True
            # comment old code

            #
        except Exception as e:
            print(f"[ERROR] Failed to click on Sales Opportunity: {e}")
            return False


    def proximity_value_submit(self):
        try:
            value = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.HOTWIRE_LENS_SALES_OPPORTUNITY_PROXIMITY)
            )
            proximity_value_suffix = value.get_attribute("value")
            proximity_value = proximity_value_suffix
            print(f'Entered Value : {proximity_value}')
            # value.clear()
            # value.send_keys(report_name1)

            proximity_submit = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(LensLocators.HOTWIRE_LENS_PROXIMITY_SUBMIT)
            )

            proximity_submit.click()
            print(f'[INFO] : CLICKED ON SALES OPPORTUNITY SUBMIT')
            return True

        except Exception as e:
            print(f'[ERROR] : Failed to submit SALES OPPORTUNITY')
            return False

    def change_value_capture_message(self):
        try:
            print("[INFO]: Right-clicked on the red-colored area (estimated position).")

            # old code
            canvas = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "mapboxgl-canvas"))
            )
            width = canvas.size['width']
            height = canvas.size['height']
            center_x = width // 2
            center_y = height // 2

            offset_x = center_x
            offset_y = center_y
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, center_x, center_y).click_and_hold(canvas).perform()
            print("[INFO]: right click happend...")

            # selecting ISP footprint
            # Hover and click "ISP Footprint Report"
            sales_opportunity1 = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.HOTWIRE_LENS_SALES_OPPORTUNITY)
            )
            time.sleep(2)
            sales_opportunity1.click()
            # actions.move_to_element(sales_opportunity).click_and_hold().click().perform()

            print('[INFO] : CLICKED ON SALES OPPORTUNITY')

            value = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.HOTWIRE_LENS_SALES_OPPORTUNITY_PROXIMITY)
            )
            proximity_value_suffix = value.get_attribute("value")
            proximity_value = proximity_value_suffix
            print(f'Old Value : {proximity_value}')
            value.clear()

            value.send_keys(PROXIMITY_VALUE)
            print(f'New Value : {PROXIMITY_VALUE}')

            proximity_submit = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(LensLocators.HOTWIRE_LENS_PROXIMITY_SUBMIT)
            )

            proximity_submit.click()
            print(f'[INFO] : CLICKED ON SALES OPPORTUNITY SUBMIT')

            #capturing toast message

            toast_element = self.wait_for_element(LensLocators.HOTWIRE_PROXIMITY_TOAST_MESSAGE)
            print(f'[INFO] : CONFIRMATION MESSAGE - {toast_element.text}')
            time.sleep(1)

            cancel = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable(LensLocators.HOTWIRE_LENS_PROXIMITY_CANCEL)
            )
            time.sleep(2)
            cancel.click()
            return True

        except Exception as e:
            print(f'[ERROR] : Failed to submit SALES OPPORTUNITY')
            return False


    def switch_to_google_window(self):
        try:
            parent_window = self.driver.current_window_handle
            print("[INFO]: Right-clicked on the red-colored area (estimated position).")

            parent_window = self.driver.current_window_handle

            # old code
            canvas = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "mapboxgl-canvas"))
            )
            width = canvas.size['width']
            height = canvas.size['height']
            center_x = width // 2
            center_y = height // 2

            offset_x = center_x
            offset_y = center_y
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, center_x, center_y).click_and_hold(canvas).perform()
            print("[INFO]: right click happend...")

            # selecting ISP footprint
            # Hover and click "ISP Footprint Report"
            google_view = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.CONTEXT_MENU_GOOGLE_VIEW)
            )
            time.sleep(2)
            google_view.click()
            # actions.move_to_element(google_view).click_and_hold().click().perform()
            # time.sleep(2)
            print(f'[INFO] : CLICKED ON {CONTEXT_MENU_GOOGLE_VIEW_VALUE}')

            WebDriverWait(self.driver, 10).until(EC.new_window_is_opened(self.driver.window_handles))
            print("[INFO]: New window opened")

            # switch to the latest window
            self.driver.switch_to.window(self.driver.window_handles[-1])

            #validation
            actual_title = WebDriverWait(self.driver, 10).until(lambda d: d.title)
            print(f"[INFO]: Google window title = {actual_title}")

            # expected value (can be parameterized)
            expected_title = '28°33\'03.1"N 81°19\'03.8"W - Google Maps'

            # compare expected vs actual
            if "Google Maps" in actual_title.strip():
                print(f"[INFO]: ✅ Title matched expected value\n"
                      f"Title : {actual_title}")
                print(f'[INFO] : CURRENT URL : {self.driver.current_url}')

            else:
                print(f"[ERROR]: Title mismatch -> Expected: {expected_title}, Got: {actual_title}")

            time.sleep(5)


            self.driver.close()  # optional: close Google window
            self.driver.switch_to.window(parent_window)
            print("[INFO]: Switched back to parent window")
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO CLICK ON GOOGLE VIEW')
            return False





