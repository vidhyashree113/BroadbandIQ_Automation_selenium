import os
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from ..config.config import *
from ..locators.right_icon_locators import RightIconLocators
from ..pages.common import BasePage
from ..locators.context_menu_locators import Context_Menu_Locators

class EXPORT_PDF_EXCEL(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def upload_geojson_to_export_report(self):
        wait = WebDriverWait(self.driver, 20)

        aoi_icon = wait.until(EC.element_to_be_clickable(RightIconLocators.UPLOAD_AOI_TOOL))
        aoi_icon.click()

        file_path = os.path.abspath(os.path.expanduser("~/Downloads/Ector_county.geojson"))

        upload_input = wait.until(EC.presence_of_element_located(RightIconLocators.CHOOSE_FILE))
        upload_input.send_keys(file_path)

        time.sleep(20)
        submit_button = wait.until(EC.presence_of_element_located(RightIconLocators.SUBMIT_AOI))
        submit_button.click()

        time.sleep(10)
        # time.sleep(3)
        error_text = self.driver.find_elements(*Context_Menu_Locators.UPLOAD_STATUS_VALUE)

        if error_text:
            error_value = error_text[0].text.strip()  # exatrcting error text and removing space at leading and trailing side
            assert not error_value, f"Upload Submit failed : {error_value}"

        actions = ActionChains(self.driver)

        map_element = wait.until(EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Map']")))
        actions.context_click(map_element).perform()

        mark_area_of_interest = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Mark as Area of Interest']")))
        mark_area_of_interest.click()

    def right_click_export_pdf(self):
        try:
            print("[INFO]: Right-clicked on the red-colored area (estimated position).")

            canvas = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "mapboxgl-canvas"))
            )
            width = canvas.size['width']
            height = canvas.size['height']
            center_x = width // 2
            center_y = height // 2

            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, center_x, center_y).context_click().perform()
            print("[INFO]: Right-click happened.")

            export_first = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(.,'Export')]"))
            )
            actions.move_to_element(export_first).click().perform()
            time.sleep(2)

            # Click "Export Report" to reveal the submenu
            export_report = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "(//a[contains(.,'Export Report')])[2]"))
            )
            export_report.click()  # ✅ Must click (not hover)
            print("[INFO]: Export Report clicked")

            # Wait and click "Export as PDF"
            export_pdf = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[.='PDF']"))
            )
            export_pdf.click()
            print('[INFO]: Export PDF clicked')

            # Description input
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.ID, "report-description"))
            )
            textarea.send_keys("Export report PDF")

            # Submit
            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "add_report_submit_btn"))
            )
            submit_btn.click()

            print("[INFO]: Export Report PDF submitted successfully.")
            return True

        except Exception as e:
            print(f"[ERROR] Export Report PDF flow failed: {e}")
            return False

    def right_click_export_excel(self):
        try:
            print("[INFO]: Right-clicked on the red-colored area (estimated position).")

            canvas = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "mapboxgl-canvas"))
            )
            width = canvas.size['width']
            height = canvas.size['height']
            center_x = width // 2
            center_y = height // 2

            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, center_x, center_y).context_click().perform()
            print("[INFO]: Right-click happened.")

            export_first = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(.,'Export')]"))
            )
            actions.move_to_element(export_first).click().perform()
            time.sleep(2)

            # Click on Export Report to open submenu
            export_report = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "(//a[contains(.,'Export Report')])[2]"))
            )
            export_report.click()
            print("[INFO]: Export Report clicked")

            # Click Export as Excel
            export_excel = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[.='Excel']"))
            )
            export_excel.click()
            print('[INFO]: Export Excel clicked')

            # Enter description
            textarea = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.ID, "export-excel-report-description"))
            )
            textarea.send_keys("Export report Excel")
            time.sleep(1)

            # Submit
            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "export_excel_report_submit_btn"))
            )
            submit_btn.click()

            print("[INFO]: Export Report Excel submitted successfully.")
            return True

        except Exception as e:
            print(f"[ERROR] Export Excel flow failed: {e}")
            return False
