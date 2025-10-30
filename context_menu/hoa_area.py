#AOI

import random
from idlelib.query import Query

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

class Hoa_Area1(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.start_time = None
        self.end_time = None
        self.driver = driver
        self.report_name = ''


    def wait_for_toast_text(self, expected_text, timeout=60, poll_frequency=1):
        by, value = Context_Menu_Locators.NOTIFICATION_ALERT
        # print("[DEBUG] Waiting for toast text...")
        try:
            wait = WebDriverWait(
                self.driver,
                timeout=timeout,
                poll_frequency=poll_frequency,
                ignored_exceptions=[NoSuchElementException]
            )
            return wait.until(lambda driver: expected_text.lower() in driver.find_element(by, value).text.lower())
        except TimeoutException as t:
            print(f"[TIMEOUT]: Toast with text '{expected_text}' not found within {timeout}s")
            raise t


    def right_click_mark_AOI(self):
        try:
            # assert self.zoom_in_button(), "[ERROR] Initial zoom in failed"
            # time.sleep(3)
            canvas = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mapboxgl-canvas"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", canvas)
            time.sleep(1)

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
            time.sleep(1)
            return True
        except Exception as e:
            print(e)
            print('[ERROR] : FAILED TO RIGHT CLICK AND SELECT MARK AREA OF INTEREST')
            return False


    # def right_click_geology_report(self):
    #     try:
    #         time.sleep(1)
    #         canvas = WebDriverWait(self.driver, 30).until(
    #             EC.element_to_be_clickable((By.CLASS_NAME, "mapboxgl-canvas"))
    #         )
    #         width = canvas.size['width']
    #         height = canvas.size['height']
    #         center_x = width // 2
    #         center_y = height // 2
    #         offset_x = 30
    #
    #         # target_x = int(width * 0.66)  # 68% from left → near top-right edge #0.68 (try 0.7, 0.66)
    #         # target_y = int(height * 0.2)  #0.18 (try 0.15, 0.2)
    #         actions = ActionChains(self.driver)
    #         actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
    #         print("[INFO]: right click happend...")
    #
    #         #right click on selecting geology export
    #         # actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
    #         # print("[INFO]: right click happend successfully...")
    #
    #         export_geology = WebDriverWait(self.driver, 50).until(
    #             EC.visibility_of_element_located(Context_Menu_Locators.GEOLOGY_REPORT)
    #         )
    #         actions.move_to_element(export_geology).click().perform()
    #         print("[INFO]: CLICKED ON EXPORT GEOLOGY REPORT SUCCESSFULLY")
    #         time.sleep(1)
    #         return True
    #
    #     except Exception as e:
    #         print('[ERROR] : FAILED TO RIGHT CLICK AND SELECT GEOLOGY REPORT')
    #         return False
    #
    #
    # def details_geology_report(self):
    #     try:
    #         value = WebDriverWait(self.driver, 30).until(
    #             EC.visibility_of_element_located(Context_Menu_Locators.PROJECT_NAME)
    #         )
    #         report_name = value.get_attribute("value")
    #         with open("report_name.txt", "w", encoding="utf-8") as f:
    #             f.write(report_name)
    #
    #         # self.report_name = report_name
    #         # print(data)
    #
    #         #entering the description:
    #         # description_message = WebDriverWait(self.driver,30).until(
    #         #     EC.visibility_of_element_located(Locators.GEO_DESCRIPTION)
    #         # )
    #         description_message = self.wait_for_element(Context_Menu_Locators.GEO_DESCRIPTION)
    #         msg = f'{report_name} generated successfully by AUTOMATION'
    #         description_message.send_keys(msg)
    #         print("[INFO]: DESCRIPTION ADDED INTO TEXT_AREA..")
    #         time.sleep(1)
    #
    #         #clicking on SUBMIT
    #
    #         geo_submit = WebDriverWait(self.driver,30).until(
    #             EC.element_to_be_clickable(Context_Menu_Locators.GEO_SUBMIT)
    #         )
    #         geo_submit.click()
    #         # self.start_time = time.time()
    #         print("[INFO]: CLICKED ON SUBMIT BUTTON")
    #         time.sleep(1)
    #         print(self.report_name)
    #         return True
    #
    #     except Exception as e:
    #         print('[ERROR]: FAILED TO CLICK ON SUBMIT BUTTON')
    #         return False

    def wait_for_download_pdf_excel_file(self, download_dir=os.path.expanduser("~/Downloads"), timeout=80, poll_frequency=2):
        before = set(os.listdir(download_dir))
        end_time = time.time() + timeout

        while time.time() < end_time:
            after = set(os.listdir(download_dir))
            new_files = after - before
            for file in new_files:
                if not file.endswith(".crdownload"):  # Ignore incomplete Chrome downloads
                    print(f"[INFO] : New file downloaded: {file}")
                    return file
            time.sleep(poll_frequency)

        raise TimeoutError("[ERROR] No new file downloaded within timeout.")

    def export_aoi(self):
        try:
            time.sleep(1)
            canvas = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "mapboxgl-canvas"))
            )
            width = canvas.size['width']
            height = canvas.size['height']
            center_x = width // 2
            center_y = height // 2
            offset_x = 30

            # target_x = int(width * 0.66)  # 68% from left → near top-right edge #0.68 (try 0.7, 0.66)
            # target_y = int(height * 0.2)  #0.18 (try 0.15, 0.2)
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
            print("[INFO]: right click happend...")

            #right click on selecting geology export
            # actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
            # print("[INFO]: right click happend successfully...")

            export_aoi = WebDriverWait(self.driver, 50).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_AOI)
            )
            actions.move_to_element(export_aoi).click().perform()
            print("[INFO]: CLICKED ON EXPORT AOI SUCCESSFULLY")
            time.sleep(1)

            export_aoi_submit = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(Context_Menu_Locators.EXPORT_AOI_SUBMIT)
            )
            export_aoi_submit.click()
            print("[INFO] : CLICKED ON EXPORT AOI SUBMIT")
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO RIGHT CLICK AND SELECT EXPORT AOI')
            return False


    def add_to_sales_territory(self):
        try:
            time.sleep(1)
            canvas = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "mapboxgl-canvas"))
            )
            width = canvas.size['width']
            height = canvas.size['height']
            center_x = width // 2
            center_y = height // 2
            offset_x = 30

            # target_x = int(width * 0.66)  # 68% from left → near top-right edge #0.68 (try 0.7, 0.66)
            # target_y = int(height * 0.2)  #0.18 (try 0.15, 0.2)
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
            print("[INFO]: right click happend...")

            #right click on selecting geology export
            # actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
            # print("[INFO]: right click happend successfully...")

            add_sales_territory = WebDriverWait(self.driver, 50).until(
                EC.visibility_of_element_located(Context_Menu_Locators.ADD_SALES_TERRITORY)
            )
            actions.move_to_element(add_sales_territory).click().perform()
            print("[INFO]: CLICKED ON ADD TO SALES TERRITORY SUCCESSFULLY")
            time.sleep(1)

            description_message = self.wait_for_element(Context_Menu_Locators.SALES_TERRITORY_DESCRIPTION)
            description_message.send_keys(SALES_TERRITORY_DESCRIPTION)
            print("[INFO]: DESCRIPTION ADDED INTO TEXT_AREA..")
            time.sleep(1)

            sales_territory_submit = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(Context_Menu_Locators.SALES_TERRITORY_SUBMIT)
            )
            sales_territory_submit.click()
            print("[INFO] : CLICKED ON SALES TERRITORY SUBMIT")
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO RIGHT CLICK AND SELECT ADD TO SALES TERRITORY')
            return False


    def network_distribution(self):
        try:
            time.sleep(1)
            canvas = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "mapboxgl-canvas"))
            )
            width = canvas.size['width']
            height = canvas.size['height']
            center_x = width // 2
            center_y = height // 2
            offset_x = 30

            # target_x = int(width * 0.66)  # 68% from left → near top-right edge #0.68 (try 0.7, 0.66)
            # target_y = int(height * 0.2)  #0.18 (try 0.15, 0.2)
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
            print("[INFO]: right click happend...")


            export_aoi = WebDriverWait(self.driver, 50).until(
                    EC.visibility_of_element_located(Context_Menu_Locators.NETWORK_DISTRIBUTION)
                )
            actions.move_to_element(export_aoi).click().perform()
            print("[INFO]: CLICKED ON NETWORK DISTRIBUTION SUCCESSFULLY")
            time.sleep(1)

            value = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.ND_PROJECT_NAME)
            )
            report_name_suffix = value.get_attribute("value")
            report_name1 = report_name_suffix
            value.clear()
            value.send_keys(report_name1)
            with open("report_name1.txt", "w", encoding="utf-8") as f:
                f.write(report_name1)

            # print(f"[INFO] Report name written to file: {report_path}")

            msg = f'{report_name1} generated successfully by AUTOMATION'

            network_description = WebDriverWait(self.driver,20).until(
                EC.visibility_of_element_located(Context_Menu_Locators.NETWORK_DISTRIBUTION_DESCRIPTION))

            network_description.send_keys(msg)
            print(f'INFO : Description Message entered --> {msg}')

            network_description_submit = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.NETWORK_DISTRIBUTION_SUBMIT)
            )


            network_description_submit.click()
            print("[INFO] : CLICKED ON NETWORK DISTRIBUTION SUBMIT")

            return True

        except Exception as e:
            print('[ERROR] : FAILED TO RIGHT CLICK AND SELECT NETWORK DISTRIBUTION')
            return False



    def capturing_toast_message(self):
        try:
            self.start_time = time.time()
            with open("report_name1.txt", "r", encoding="utf-8") as f:
                report_name = f.read().strip()
            print(f"[INFO] Report name read from file: '{report_name}'")
            text2 = f"The request for the Network Distribution Path has been successfully submitted. Notification will be sent once the path is generated and ready."
            text3 = f"The Network distribution {report_name} has been completed . Please click the map button to view it."

            print(f"[WAITING] : Toast Accepted --> {text2}")
            if not self.wait_for_toast_text(text2, timeout=90):
                print(f"[ERROR] Toast not found for: {text2}")
                return False
            print("[SUCCESS]: All toasts received and verified.")

            print(f"[WAITING]: Toast: Completed --> {text3}")
            if not self.wait_for_toast_text(text3, timeout=600):
                print(f"[ERROR] Toast not found for: {text3}")
                return False
            print("[SUCCESS]: All toasts received and verified.")


            close = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(Context_Menu_Locators.TOAST_CLOSE)
            )
            close.click()
            print('[INFO]: CLICKED ON TOAST CLOSE..')

            self.end_time = time.time()
            total_time = self.end_time - self.start_time
            minutes = int(total_time // 60)
            seconds = total_time % 60
            # print(f'Time taken to complete PDF and KMZ download is {minutes} minutes and {seconds:.2f} seconds')
            print(f'Time taken to complete PDF and KMZ download is {minutes} minutes and {round(seconds)} seconds')
            return True

        except Exception as e:
            print(f'[ERROR] : FAILED TO CAPTURE TOAST MESSAGE: {e}')
            return False

    def right_click_export_pdf(self):
        try:

            print("[INFO]: Right-clicked on the red-colored area (estimated position).")

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

            # selecting ISP footprint
            # Hover and click "ISP Footprint Report"
            service = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_BUTTON)
            )
            actions.move_to_element(service).click().perform()


            export_report = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_EXPORT_REPORT_BUTTON)
            )
            actions.move_to_element(export_report).click().perform()

            #commented code
            # state = WebDriverWait(self.driver, 30).until(
            #     EC.visibility_of_element_located((By.XPATH, "//a[contains(.,'Export Report')]//a[.='Export as PDF']"))
            # )
            # actions.move_to_element(state).click().perform()
            # print('[INFO]: Export PDF clicked')
            # time.sleep(2)

            state = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_EXPORT_PDF)
            )
            actions.move_to_element(state).click().perform()
            print('[INFO]: Export PDF clicked')


            # Enter description
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.ID, "report-description"))
            )
            textarea.send_keys("Export report PDF")



            # Click submit
            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "add_report_submit_btn"))
            )
            submit_btn.click()

            downloaded_file = self.wait_for_download_pdf_excel_file()
            print(f"[INFO]: Export Report PDF downloaded successfully: {downloaded_file}")

            # print("[INFO]: Export Report PDF export submitted successfully.")
            return True
            #comment old code

        #
        except Exception as e:
            # print(f"[ERROR] Export Report PDF flow failed: {e}")
            return False

    def right_click_export_excel(self):
        try:

            print("[INFO]: Right-clicked on the red-colored area (estimated position).")

            #old code
            canvas = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "mapboxgl-canvas"))
            )
            width = canvas.size['width']
            height = canvas.size['height']
            center_x = width // 2
            center_y = height // 2

            offset_x = center_x
            offset_y = center_y
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
            print("[INFO]: right click happend...")

            # selecting ISP footprint
            # Hover and click "ISP Footprint Report"

            service = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_BUTTON)
            )
            actions.move_to_element(service).click().perform()
            time.sleep(2)

            export_report = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_EXPORT_REPORT_BUTTON)
            )
            actions.move_to_element(export_report).click().perform()

            # service = WebDriverWait(self.driver, 30).until(
            #     EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_BUTTON)
            # )
            # actions.move_to_element(service).click().perform()
            # time.sleep(2)

            state = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_EXPORT_EXCEL)
            )
            actions.move_to_element(state).click().perform()
            print('[INFO]: Export Excel clicked')



            # Enter description
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_SERVICE_EXPORT_EXCEL_TEXTAREA)
            )
            textarea.send_keys("Export report Excel")

            time.sleep(2)

            # Click submit
            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.EXOPRT_SERVICE_EXPORT_EXCEL_SUBMIT)
            )
            submit_btn.click()
            downloaded_file = self.wait_for_download_pdf_excel_file()
            print(f"[INFO]: Export Report Excel downloaded successfully: {downloaded_file}")

            # print("[INFO]: Export Report Excel export submitted successfully.")
            return True
            #comment old code

        #
        except Exception as e:
            # print(f"[ERROR] Export Excel flow failed: {e}")
            return False







