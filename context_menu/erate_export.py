

#City_Code

import random
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from ..config.config import *
# from config.assertion_config import *
from ..locators.context_menu_locators import Context_Menu_Locators
from ..locators.right_icon_locators import RightIconLocators
from ..pages.map_page import MapPage
from ..pages.common import BasePage
from datetime import datetime
import time,os

# import time

class ErateExport(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def right_click_mark_AOI(self):
        try:

            # time.sleep(5)
            canvas = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(Context_Menu_Locators.ERATE_RIGHT_CLICK)
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

    def wait_for_download_pdf_excel_file(self, download_dir=os.path.expanduser("~/Downloads"), timeout=80, poll_frequency=2):
        before = set(os.listdir(download_dir))
        end_time = time.time() + timeout

        while time.time() < end_time:
            after = set(os.listdir(download_dir))
            new_files = after - before
            for file in new_files:
                if not file.endswith(".crdownload"):  # Ignore incomplete Chrome downloads
                    print(f"[INFO] New file downloaded: {file}")
                    return file
            time.sleep(poll_frequency)

        raise TimeoutError("[ERROR] No new file downloaded within timeout.")


    def right_click_erate_export_pdf(self):
        try:
            print("[INFO]: Right-clicked on the red-colored area (estimated position).")

            #old code
            canvas = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.ERATE_RIGHT_CLICK)
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
                EC.visibility_of_element_located(Context_Menu_Locators.ERATE_EXPORT_BUTTON)
            )
            actions.move_to_element(service).click().perform()
            time.sleep(2)

            export_report = WebDriverWait(self.driver,30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.ERATE_EXPORT_REPORT_BUTTON)
            )
            actions.move_to_element(export_report).click().perform()



            #commented code
            state = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.ERATE_EXPORT_PDF)
            )
            actions.move_to_element(state).click().perform()
            print('[INFO]: Export PDF clicked')
            time.sleep(2)

            # Enter description
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.ERATE_EXPORT_TEXTAREA)
            )
            textarea.send_keys("Export report Erate PDF")

            time.sleep(2)

            # Click submit
            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.ERATE_EXPORT_SUBMIT_BUTTON)
            )
            submit_btn.click()

            # downloaded_file = self.wait_for_download_pdf_excel_file()
            # print(f"[INFO]: Export Report PDF downloaded successfully: {downloaded_file}")


            return True
            #comment old code

        #
        except Exception as e:
            # print(f"[ERROR] Export Report PDF flow failed: {e}")
            return False

    def right_click_erate_export_excel(self):
        try:
            print("[INFO]: Right-clicked on the red-colored area (estimated position).")
            time.sleep(20)
            self.driver.execute_script("document.body.style.zoom='80%'")

            #old code
            canvas = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.ERATE_RIGHT_CLICK)
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
                EC.visibility_of_element_located(Context_Menu_Locators.ERATE_EXPORT_BUTTON)
            )
            actions.move_to_element(service).click().perform()
            time.sleep(2)


            export_report = WebDriverWait(self.driver,30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.ERATE_EXPORT_REPORT_BUTTON)
            )
            actions.move_to_element(export_report).click().perform()


            #commented code
            state = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.ERATE_EXPORT_EXCEL)
            )
            actions.move_to_element(state).click().perform()
            print('[INFO]: Export Excel clicked')
            time.sleep(2)

            # Enter description
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.ERATE_EXPORT_EXCEL_TEXTAREA)
            )
            textarea.send_keys("Export report Erate Excel")

            time.sleep(2)

            # Click submit
            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.ERATE_EXPORT_EXCEL_SUBMIT_BUTTON)
            )
            submit_btn.click()
            time.sleep(10)
            print("[INFO]: Export Report Excel export submitted successfully.")

            downloaded_file = self.wait_for_download_pdf_excel_file()
            print(f"[INFO]: Export Report Excel downloaded successfully: {downloaded_file}")

            self.driver.execute_script("document.body.style.zoom='100%'")
            return True
            #comment old code

        #
        except Exception as e:
            # print(f"[ERROR] Export Excel flow failed: {e}")
            return False