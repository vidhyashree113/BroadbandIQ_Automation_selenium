# from traceback import print_tb
import os

import pytest
from prettytable import PrettyTable
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..config.assertion_config import POLE_OWNER_LABELS
from ..locators.right_icon_locators import RightIconLocators
import time
from ..locators.context_menu_locators import Context_Menu_Locators
from ..config.config import *
from ..pages.common import BasePage


class CommonContextMenu(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

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


    def service_covereage_state_pdf(self):
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
                EC.visibility_of_element_located(Context_Menu_Locators.SERVICE_COVERAGE)
            )
            actions.move_to_element(service).click().perform()
            time.sleep(1)


            #commented code
            state = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.SERVICE_COVERAGE_STATE)
            )
            actions.move_to_element(state).click().perform()
            print('[INFO]: State clicked')
            time.sleep(1)

            # Hover and click "PDF Report"
            pdf = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.SERVICE_COVERAGE_STATE_PDF)
            )
            actions.move_to_element(pdf).click().perform()
            print("[INFO]: PDF report clicked")
            time.sleep(1)

            # Enter description
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.SERVICE_COVERAGE_STATE_COUNTY_PDF_TEXTAREA)
            )
            textarea.send_keys("PDF")

            time.sleep(2)

            # Click submit
            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.SERVICE_COVERAGE_STATE_COUNTY_PDF_SUBMIT)
            )
            submit_btn.click()

            downloaded_file = self.wait_for_download_pdf_excel_file()
            print(f"[INFO]: SERVICE COVERAGE STATE PDF downloaded successfully: {downloaded_file}")

            # print("[INFO]: Service coverage State PDF export submitted successfully.")

            return True
            #comment old code
        except Exception as e:
            print(f"[ERROR] Service coverage State PDF flow failed: {e}")
            return False

    def service_covereage_state_excel(self):
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

            offset_x = center_x + 30
            offset_y = center_y
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
            print("[INFO]: right click happend...")

            # selecting ISP footprint
            # Hover and click "ISP Footprint Report"
            service = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.SERVICE_COVERAGE)
            )
            actions.move_to_element(service).click().perform()
            time.sleep(1)

            # commented code
            state = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.SERVICE_COVERAGE_STATE)
            )
            actions.move_to_element(state).click().perform()
            print('[INFO]: State clicked')
            time.sleep(1)

            # Hover and click "PDF Report"
            pdf = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.SERVICE_COVERAGE_STATE_EXCEL)
            )
            actions.move_to_element(pdf).click().perform()
            print("[INFO]: Excel report clicked")
            time.sleep(1)

            # Enter description
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.SERVICE_COVERAGE_STATE_COUNTY_EXCEL_TEXTAREA)
            )
            textarea.send_keys("Excel")

            time.sleep(2)

            # Click submit
            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.SERVICE_COVERAGE_STATE_COUNTY_EXCEL_SUBMIT)
            )
            submit_btn.click()
            downloaded_file = self.wait_for_download_pdf_excel_file()
            print(f"[INFO]: SERVICE COVERAGE STATE EXCEL downloaded successfully: {downloaded_file}")

            # print("[INFO]: Service coverage State Excel export submitted successfully.")
            return True
            # comment old code
        except Exception as e:
            print(f"[ERROR] Service coverage State Excel flow failed: {e}")
            return False



    def service_covereage_county_pdf(self):
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

            offset_x = center_x + 30
            offset_y = center_y
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
            print("[INFO]: right click happend...")

            # selecting ISP footprint
            # Hover and click "ISP Footprint Report"
            service = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.SERVICE_COVERAGE)
            )
            actions.move_to_element(service).click().perform()
            time.sleep(1)

            # commented code
            state = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.SERVICE_COVERAGE_COUNTY)
            )
            actions.move_to_element(state).click().perform()
            print('[INFO]: County clicked')
            time.sleep(1)

            # Hover and click "PDF Report"
            pdf = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.SERVICE_COVERAGE_COUNTY_PDF)
            )
            actions.move_to_element(pdf).click().perform()
            print("[INFO]: County PDF report clicked")
            time.sleep(1)

            # Enter description
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.SERVICE_COVERAGE_STATE_COUNTY_PDF_TEXTAREA)
            )
            textarea.send_keys("COUNTY PDF")

            time.sleep(2)

            # Click submit
            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.SERVICE_COVERAGE_STATE_COUNTY_PDF_SUBMIT)
            )
            submit_btn.click()
            downloaded_file = self.wait_for_download_pdf_excel_file()
            print(f"[INFO]: SERVICE COVERAGE COUNTY PDF downloaded successfully: {downloaded_file}")

            # print("[INFO]: Service coverage State Excel export submitted successfully.")
            return True
            # comment old code
        except Exception as e:
            print(f"[ERROR] Service coverage County PDF flow failed: {e}")
            return False


    def service_covereage_county_excel(self):
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

            offset_x = center_x + 30
            offset_y = center_y
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
            print("[INFO]: right click happend...")

            # selecting ISP footprint
            # Hover and click "ISP Footprint Report"
            service = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.SERVICE_COVERAGE)
            )
            actions.move_to_element(service).click().perform()
            time.sleep(1)

            # commented code
            state = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.SERVICE_COVERAGE_COUNTY)
            )
            actions.move_to_element(state).click().perform()
            print('[INFO]: County clicked')
            time.sleep(1)

            # Hover and click "PDF Report"
            pdf = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.SERVICE_COVERAGE_COUNTY_EXCEL)
            )
            actions.move_to_element(pdf).click().perform()
            print("[INFO]: County EXCEL report clicked")
            time.sleep(1)

            # Enter description
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.SERVICE_COVERAGE_STATE_COUNTY_EXCEL_TEXTAREA)
            )
            textarea.send_keys("COUNTY EXCEL")

            time.sleep(2)

            # Click submit
            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.SERVICE_COVERAGE_STATE_COUNTY_EXCEL_SUBMIT)
            )
            submit_btn.click()
            downloaded_file = self.wait_for_download_pdf_excel_file()
            print(f"[INFO]: SERVICE COVERAGE COUNTY EXCEL downloaded successfully: {downloaded_file}")

            # print("[INFO]: Service coverage State Excel export submitted successfully.")
            return True
            # comment old code
        except Exception as e:
            print(f"[ERROR] Service coverage County EXCEL flow failed: {e}")
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
            print('[INFO] : RIGHT CLICK HAPPENED SUCCESSFULLY')
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
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_EXPORT_PDF)
            )
            actions.move_to_element(state).click().perform()
            print('[INFO]: Export PDF clicked')



            # Enter description
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_EXPORT_PDF_TEXTAREA)
            )
            textarea.send_keys("Export report PDF")

            time.sleep(2)

            # Click submit
            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.EXPORT_EXPORT_PDF_SUBMIT)
            )
            submit_btn.click()
            downloaded_file = self.wait_for_download_pdf_excel_file()
            print(f"[INFO]: Export PDF downloaded successfully: {downloaded_file}")

            # print("[INFO]: Export Report Excel export submitted successfully.")
            return True
            #comment old code

        #
        except Exception as e:
            print(f"[ERROR] Export PDF flow failed: {e}")
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
            print('[INFO] : RIGHT CLICK HAPPENED SUCCESSFULLY')
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
            print('[INFO]: Export EXCEL clicked')



            # Enter description
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_EXPORT_EXCEL_TEXTAREA)
            )
            textarea.send_keys("Export report PDF")

            time.sleep(2)

            # Click submit
            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.EXPORT_EXPORT_EXCEL_SUBMIT_BUTTON)
            )
            submit_btn.click()
            downloaded_file = self.wait_for_download_pdf_excel_file()
            print(f"[INFO]: Export EXCEL downloaded successfully: {downloaded_file}")

            return True
            #comment old code

        #
        except Exception as e:
            print(f"[ERROR] Export EXCEL flow failed: {e}")
            return False