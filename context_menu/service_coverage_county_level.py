
# from traceback import print_tb

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..locators.right_icon_locators import RightIconLocators
import time
from ..locators.context_menu_locators import Context_Menu_Locators
from ..config.config import *
from ..pages.common import BasePage
from ..pages.map_page import MapPage
from selenium.webdriver.support.select import Select
import traceback


class ServiceCoverage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver


    def right_click_service_coverage_county_pdf_report(self):
        try:
            print("[INFO] Starting right-click on service coverage map...")

            # Locate the map canvas and right-click on center + offset
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

            # Step 1: Hover and click "Service Coverage Report"
            service_report = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'Service Coverage Report')]"))
            )
            ActionChains(self.driver).move_to_element(service_report).click().perform()
            print("[INFO] Clicked on 'Service Coverage Report'")

            time.sleep(1)

            # Step 2: Click "County"
            county_option = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located
                    ((By.XPATH, "//a[contains(.,'Service Coverage Report')]/following::a[text()='County']"))
            )
            ActionChains(self.driver).move_to_element(county_option).click().perform()
            print("[INFO] Clicked on 'County' option")

            time.sleep(1)

            # Step 3: Click "PDF Report"
            pdf_option = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located
                    ((By.XPATH, "(//a[contains(.,'Service Coverage Report')]/following::a[text()='PDF Report'])[2]"))
            )
            ActionChains(self.driver).move_to_element(pdf_option).click().perform()
            print("[INFO] Clicked on 'PDF Report'")

            time.sleep(2)

            # Step 4: Enter description
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.ID, "state-county-report-description"))
            )
            textarea.clear()
            textarea.send_keys("COUNTY PDF")
            print("[INFO] Entered report description")

            # Step 5: Click Submit
            submit_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "add_state_county_report_submit_btn"))
            )
            submit_button.click()
            print("[INFO] Submitted Service Coverage County PDF report.")
            return True

        except Exception as e:
            print(f"[ERROR] Service coverage County PDF flow failed: {e}")
            return False


    def right_click_service_coverage_county_excel_report(self):
        try:
            self.driver.execute_script("document.body.style.zoom='80%'")
            time.sleep(1)
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
            actions.move_to_element_with_offset(canvas, center_x,center_y).context_click(canvas).perform()
            print("[INFO]: right click happend...")

            # selecting ISP footprint
            # Hover and click "ISP Footprint Report"
            service = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(.,'Service Coverage Report')]"))
            )
            actions.move_to_element(service).click().perform()
            time.sleep(2)


            #commented code
            county = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(.,'Service Coverage Report')]/following::a[text()='County']"))
            )
            actions.move_to_element(county).click().perform()
            print('[INFO]: County clicked')
            time.sleep(2)

            # Hover and click "Excel Report"
            excel = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "(//a[contains(.,'Service Coverage Report')]/following::a[text()='Excel Report'])[2]"))
            )
            actions.move_to_element(excel).click().perform()
            print("[INFO]: COUNTY EXCEL report clicked")
            time.sleep(2)
            #
            # # Hover and click "PDF Report"
            # isp_pdf = WebDriverWait(self.driver, 30).until(
            #     EC.visibility_of_element_located((By.XPATH, "(//a[contains(.,'ISP Footprint Report')]/following::a[text()='PDF Report'])[1]"))
            # )
            # actions.move_to_element(isp_pdf).click().perform()
            # print('[INFO] : Clicked on PDF')
            # time.sleep(2)

            # Enter description
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.ID, "state-county-excel-report-description"))
            )
            textarea.send_keys("County Excel")

            time.sleep(2)

            # Click submit
            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "state_county_excel_report_submit_btn"))
            )
            submit_btn.click()

            print("[INFO]: County Excel export submitted successfully.")
            time.sleep(2)
            self.driver.execute_script("document.body.style.zoom='100%'")
            return True
            #comment old code
        #
        except Exception as e:
            print(f"[ERROR] Service coverage County flow failed: {e}")
            return False

    def zoom_out_button(self):
        try:
            # Scrolling up:

            # scroll = WebDriverWait(self.driver, 20).until(
            #     EC.visibility_of_element_located(RightIconLocators.GEOLOGY_ICON)
            # )
            # top = scroll.location
            self.driver.execute_script("window.scrollTo(0,0)")
            zoom = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(RightIconLocators.ZOOM_OUT)
            )
            zoom.click()
            print('[INFO] : CLICKED ON ZOOM OUT ICON')
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO ZOOM OUT')
            return False