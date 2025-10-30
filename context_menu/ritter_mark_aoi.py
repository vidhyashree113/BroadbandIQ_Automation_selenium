#AOI

import random
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from ..config.config import *
# from config.assertion_config import *
from ..locators.context_menu_locators import Context_Menu_Locators
from ..pages.map_page import MapPage
from ..pages.common import BasePage
from datetime import datetime
import time,os
from bs4 import BeautifulSoup
# import time

class Ritter_mark_aoi(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.start_time = None
        self.end_time = None
        self.driver = driver
        self.report_name = ''

    def drag_up_and_mark_aoi(self, steps=3, pixels_per_step=0, pause=1):
        try:
            # Step 1: Initial Zoom In
            assert self.zoom_in_button(), "[ERROR] Initial zoom in failed"
            assert self.zoom_in_button(), "[ERROR] Initial zoom in failed"
            assert self.zoom_in_button(), "[ERROR] Initial zoom in failed"

            # Step 2: Locate canvas
            canvas = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mapboxgl-canvas"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", canvas)
            time.sleep(1)

            size = canvas.size
            width = size['width']
            height = size['height']
            center_x = width // 2
            start_y = max(100, int(height * 0.2))

            print(f"[INFO] Canvas size: {width}x{height}")
            print(f"[INFO] Starting drag at ({center_x}, {start_y})")

            # Step 3: Drag upward in multiple steps
            for i in range(steps):
                print(f"[INFO] Step {i + 1}/{steps} - Dragging down by {pixels_per_step}px to move map up")
                actions = ActionChains(self.driver)
                actions.move_to_element_with_offset(canvas, center_x, start_y) \
                    .click_and_hold() \
                    .move_by_offset(0, pixels_per_step) \
                    .release() \
                    .perform()
                time.sleep(pause)

            # Step 4: Drag slightly to right
            print("[INFO] Final shift - Dragging left by 100px (to move map right)")
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, center_x, start_y) \
                .click_and_hold() \
                .move_by_offset(150, 0) \
                .release() \
                .perform()

            print("[INFO] ✅ Map repositioned")
            return True

        except Exception as e:
            print(f"[ERROR] ❌ Failed to drag and mark AOI: {e}")
            return False

    def right_click_mark_AOI(self):
        try:
            canvas = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mapboxgl-canvas"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", canvas)
            time.sleep(3)

            width = canvas.size['width']
            height = canvas.size['height']
            center_x = width // 2
            center_y = height // 2
            offset_x = 40  # Shift slightly to the right of center
            offset_y = 10
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
            print("[INFO]: right click happend...")

            # selecting MARK AREA OF INTREST
            aoi = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.MARK_AOI)
            )
            actions.move_to_element(aoi).click().perform()
            print("[INFO]: CLICKED ON MARK AOI SUCCESSFULLY")
            time.sleep(2)
            return True
        except Exception as e:
            print(e)
            print('[ERROR] : FAILED TO RIGHT CLICK AND SELECT MARK AREA OF INTEREST')
            return False

    def zoom_in_button(self):
        try:
            zoom = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(Context_Menu_Locators.ZOOM_IN)
            )
            zoom.click()
            print('[INFO] : CLICKED ON ZOOM ICON')
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO ZOOM IN')
            return False

    def right_click_ritter_export_pdf(self):
        try:
            print("[INFO]: Right-clicked on the red-colored area (estimated position).")

            canvas = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "mapboxgl-canvas"))
            )
            width = canvas.size['width']
            height = canvas.size['height']
            center_x = width // 2
            center_y = height // 2

            offset_x = center_x + 30
            offset_y = center_y
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
            print("[INFO]: right click happend...")

            export_first = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(.,'Export')]"))
            )
            actions.move_to_element(export_first).click().perform()
            time.sleep(2)

            service = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(.,'Export Report')]"))
            )
            actions.move_to_element(service).click().perform()
            time.sleep(2)

            state = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//a[.='PDF']"))
            )
            actions.move_to_element(state).click().perform()
            print('[INFO]: Export PDF clicked')
            time.sleep(2)

            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.ID, "report-description"))
            )
            textarea.send_keys("Export report ritter PDF")

            time.sleep(2)

            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "add_report_submit_btn"))
            )
            submit_btn.click()

            print("[INFO]: Export Report PDF export submitted successfully.")
            return True
            #comment old code

        #
        except Exception as e:
            return False

    def right_click_ritter_export_excel(self):
        try:
            print("[INFO]: Right-clicked on the red-colored area (estimated position).")
            time.sleep(2)
            self.driver.execute_script("document.body.style.zoom='80%'")

            canvas = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "mapboxgl-canvas"))
            )
            width = canvas.size['width']
            height = canvas.size['height']
            center_x = width // 2
            center_y = height // 2

            offset_x = center_x + 30
            offset_y = center_y
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
            print("[INFO]: right click happend...")

            export_first = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(.,'Export')]"))
            )
            actions.move_to_element(export_first).click().perform()
            time.sleep(2)

            service = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(.,'Export Report')]"))
            )
            actions.move_to_element(service).click().perform()
            time.sleep(2)


            #commented code
            state = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//a[.='Excel']"))
            )
            actions.move_to_element(state).click().perform()
            print('[INFO]: Export Excel clicked')
            time.sleep(2)

            # Enter description
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.ID, "export-excel-report-description"))
            )
            textarea.send_keys("Export report ritter Excel")

            time.sleep(2)

            # Click submit
            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "export_excel_report_submit_btn"))
            )
            submit_btn.click()

            print("[INFO]: Export Report Excel export submitted successfully.")
            self.driver.execute_script("document.body.style.zoom='100%'")

            return True
            #comment old code

        #
        except Exception as e:
            # print(f"[ERROR] Export Excel flow failed: {e}")
            return False
