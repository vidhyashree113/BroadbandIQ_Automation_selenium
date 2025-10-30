

#zipcode_Code

import random
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException

from ..locators.lens_locators import LensLocators
from ..config.config import *
# from config.assertion_config import *
from ..locators.context_menu_locators import Context_Menu_Locators
from ..locators.right_icon_locators import RightIconLocators
from ..pages.map_page import MapPage
from ..pages.common import BasePage
from datetime import datetime
import time,os
from bs4 import BeautifulSoup
# import time

class UploadKmz_Zipcode(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def right_click_mark_AOI(self):
        try:
            time.sleep(1)
            canvas = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "mapboxgl-canvas"))
            )
            width = canvas.size['width']
            height = canvas.size['height']
            center_x = width // 2
            center_y = height // 2
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
            print("[INFO]: right click happend...")

            # selecting MARK AREA OF INTREST
            aoi = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.MARK_AOI)
            )
            actions.move_to_element(aoi).click().perform()
            print("[INFO]: CLICKED ON MARK AOI SUCCESSFULLY")
            time.sleep(2)
            return True
        except Exception as e:
            print('[ERROR] : FAILED TO RIGHT CLICK AND SELECT MARK AREA OF INTEREST')
            return False

    def right_click_export_pdf(self):
        try:
            print("[INFO]: Right-clicked on the red-colored area (estimated position).")

            # old code
            canvas = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.EXPORT_RIGHT_CLICK)
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

            # selecting ISP footprint
            # Hover and click "ISP Footprint Report"
            service = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_EXPORT_BUTTON)
            )
            actions.move_to_element(service).click().perform()
            time.sleep(2)

            export_report = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_EXPORT_REPORT_BUTTON)
            )
            actions.move_to_element(export_report).click().perform()

            # commented code
            state = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_EXPORT_PDF)
            )
            actions.move_to_element(state).click().perform()
            print('[INFO]: Export PDF clicked')
            time.sleep(2)

            # Enter description
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_EXPORT_TEXTAREA)
            )
            textarea.send_keys("Export report Erate PDF")

            time.sleep(2)

            # Click submit
            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.EXPORT_EXPORT_SUBMIT_BUTTON)
            )
            submit_btn.click()

            # downloaded_file = self.wait_for_download_pdf_excel_file()
            # print(f"[INFO]: Export Report PDF downloaded successfully: {downloaded_file}")

            return True
            # comment old code

        #
        except Exception as e:
            # print(f"[ERROR] Export Report PDF flow failed: {e}")
            return False

    def right_click_export_excel(self):
        try:
            print("[INFO]: Right-clicked on the red-colored area (estimated position).")
            time.sleep(20)
            self.driver.execute_script("document.body.style.zoom='80%'")

            # old code
            canvas = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.EXPORT_RIGHT_CLICK)
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

            # selecting ISP footprint
            # Hover and click "ISP Footprint Report"
            service = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_EXPORT_BUTTON)
            )
            actions.move_to_element(service).click().perform()
            time.sleep(2)

            export_report = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_EXPORT_REPORT_BUTTON)
            )
            actions.move_to_element(export_report).click().perform()

            # commented code
            state = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_EXPORT_EXCEL)
            )
            actions.move_to_element(state).click().perform()
            print('[INFO]: Export Excel clicked')
            time.sleep(2)

            # Enter description
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_EXPORT_EXCEL_TEXTAREA)
            )
            textarea.send_keys("Export report Erate Excel")

            time.sleep(2)

            # Click submit
            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.EXPORT_EXPORT_EXCEL_SUBMIT_BUTTON)
            )
            submit_btn.click()
            time.sleep(10)
            print("[INFO]: Export Report Excel export submitted successfully.")

            # downloaded_file = self.wait_for_download_pdf_excel_file()
            # print(f"[INFO]: Export Report Excel downloaded successfully: {downloaded_file}")

            self.driver.execute_script("document.body.style.zoom='100%'")
            return True
            # comment old code

        #
        except Exception as e:
            # print(f"[ERROR] Export Excel flow failed: {e}")
            return False


    def zip_code_upload_aoi(self):

        try:
            wait = WebDriverWait(self.driver, 20)

            aoi_icon = wait.until(EC.element_to_be_clickable(RightIconLocators.UPLOAD_AOI_TOOL))
            aoi_icon.click()

            file_name = "77372 (Montgomery County, TX,Liberty County, TX).kmz"  # or .kmz
            file_path = os.path.abspath(os.path.join("Upload_KMZ_files", file_name))

            print(f"[INFO] Uploading file: {file_path}")

            # Step 3: Upload file
            upload_input = wait.until(EC.presence_of_element_located(RightIconLocators.CHOOSE_FILE))
            upload_input.send_keys(file_path)

            # Step 4: Wait for frontend to recognize and submit
            time.sleep(2)
            submit_button = wait.until(EC.element_to_be_clickable(RightIconLocators.AOI_SUBMIT))
            submit_button.click()
            time.sleep(3)
            error_text = self.driver.find_elements(*Context_Menu_Locators.UPLOAD_STATUS_VALUE)

            if error_text:
                error_value = error_text[0].text.strip()  # exatrcting error text and removing space at leading and trailing side
                assert not error_value, f"Upload Submit failed : {error_value}"
            print('[INFO] File Uploaded Successfully')
            return True

        except Exception as e:
            print('[ERROR] Failed to upload KMZ for city')
            return False