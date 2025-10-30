from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from ..config.config import *
from ..locators.context_menu_locators import Context_Menu_Locators
from ..pages.common import BasePage
from datetime import datetime
import time,os

class HOAExport(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def right_click_mark_AOI(self):
        try:

            # time.sleep(5)
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



    def right_click_hoa_export_pdf(self):
        try:
            print("[INFO]: Right-clicked on the hoa boundary found area (estimated position).")

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

            service = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(.,'Export Report')]"))
            )
            actions.move_to_element(service).click().perform()
            time.sleep(2)


            state = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(.,'Export Report')]//a[.='Export as PDF']"))
            )
            actions.move_to_element(state).click().perform()
            print('[INFO]: Export PDF clicked')
            time.sleep(2)

            # Enter description
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.ID, "report-description"))
            )
            textarea.send_keys("Export report bead PDF")

            time.sleep(2)

            # Click submit
            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "add_report_submit_btn"))
            )
            submit_btn.click()

            print("[INFO]: Export Report PDF export submitted successfully.")
            return True

        except Exception as e:
            # print(f"[ERROR] Export Report PDF flow failed: {e}")
            return False

    def right_click_hoa_export_excel(self):
        try:
            print("[INFO]: Right-clicked on the hoa boundary founded area (estimated position).")
            time.sleep(2)
            self.driver.execute_script("document.body.style.zoom='80%'")

            #old code
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

            service = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(.,'Export Report')]"))
            )
            actions.move_to_element(service).click().perform()
            time.sleep(2)

            state = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(.,'Export Report')]//a[.='Export as Excel']"))
            )
            actions.move_to_element(state).click().perform()
            print('[INFO]: Export Excel clicked')
            time.sleep(2)

            # Enter description
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.ID, "export-excel-report-description"))
            )
            textarea.send_keys("Export report bead Excel")

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