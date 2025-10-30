import random
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from ..config.config import *
from ..locators.context_menu_locators import Context_Menu_Locators
# from config.assertion_config import *
from ..locators.lens_locators import LensLocators
from ..pages.map_page import MapPage
from ..pages.common import BasePage
from datetime import datetime
import time,os
from bs4 import BeautifulSoup
# import time

class AreaBoundary_State_Upper(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.start_time = None
        self.end_time = None
        self.driver = driver
        self.report_name = ''

    def wait_for_toast_text(self, expected_text, timeout=60, poll_frequency=1):
        """Use FluentWait to wait until toast contains expected text."""
        by, value = Context_Menu_Locators.NOTIFICATION_ALERT
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

    def drag_up_and_mark_aoi(self, steps=3, pixels_per_step=80, pause=1):
        try:
            # Step 1: Initial Zoom In
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
                .move_by_offset(0, 0) \
                .release() \
                .perform()

            print("[INFO] ✅ Map repositioned")
            return True

        except Exception as e:
            print(f"[ERROR] ❌ Failed to drag and mark AOI: {e}")
            return False


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

            # selecting MARK AREA OF INTREST
            aoi = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.MARK_AOI)
            )
            actions.move_to_element(aoi).click().perform()
            print("[INFO]: CLICKED ON MARK AOI SUCCESSFULLY")
            time.sleep(2)
            return True
        except Exception as e:
            print(e)
            print('[ERROR] : FAILED TO RIGHT CLICK AND SELECT MARK AREA OF INTEREST')
            return False


    def right_click_geology_report(self):
        try:
            time.sleep(3)
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
            actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
            print("[INFO]: right click happend successfully...")

            export_geology = WebDriverWait(self.driver, 50).until(
                EC.visibility_of_element_located(LensLocators.GEOLOGY_REPORT)
            )
            actions.move_to_element(export_geology).click().perform()
            print("[INFO]: CLICKED ON EXPORT GEOLOGY REPORT SUCCESSFULLY")
            time.sleep(2)
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO RIGHT CLICK AND SELECT GEOLOGY REPORT')
            return False


    def details_geology_report(self):
        try:
            value = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(LensLocators.PROJECT_NAME)
            )
            report_name = value.get_attribute("value")
            with open("report_name.txt", "w", encoding="utf-8") as f:
                f.write(report_name)

            # self.report_name = report_name
            # print(data)

            #entering the description:
            description_message = WebDriverWait(self.driver,30).until(
                EC.visibility_of_element_located(LensLocators.GEO_DESCRIPTION)
            )
            msg = f'{report_name} generated successfully by AUTOMATION'
            description_message.send_keys(msg)
            print("[INFO]: DESCRIPTION ADDED INTO TEXT_AREA..")
            time.sleep(3)

            #clicking on SUBMIT

            geo_submit = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable(LensLocators.GEO_SUBMIT)
            )
            geo_submit.click()
            # self.start_time = time.time()
            print("[INFO]: CLICKED ON SUBMIT BUTTON")
            time.sleep(2)
            print(self.report_name)
            return True

        except Exception as e:
            print('[ERROR]: FAILED TO CLICK ON SUBMIT BUTTON')
            return False

            # FluentWait for each toast

    # def capturing_toast_message(self):
    #     try:
    #         self.start_time = time.time()
    #         with open("report_name.txt", "r", encoding="utf-8") as f:
    #             report_name = f.read().strip()
    #         print(f"[INFO] Report name read from file: '{report_name}'")
    #
    #         # text1 = f"The request for the Geology Analysis for  {report_name} has been received. A notification will be sent once the report is ready"
    #         # text2 = f"The request for the Geology Analysis for {report_name} is in progress. A notification will be sent once the report is ready."
    #         text3 = f"The request for the Geology Analysis for {report_name} has been completed. You can download the PDF and KMZ files here."
    #
    #         # print(f"[WAITING]: Toast: In Progress --> {text2}")
    #         # if not self.wait_for_toast_text(text2, timeout=500):
    #         #     print(f"[ERROR] Toast not found for: {text2}")
    #         #     return False
    #
    #         print(f"[WAITING]: Toast: Completed --> {text3}")
    #         if not self.wait_for_toast_text(text3, timeout=750):
    #             print(f"[ERROR] Toast not found for: {text3}")
    #             return False
    #
    #         print("[SUCCESS]: All toasts received and verified.")
    #         self.end_time = time.time()
    #         total_time = self.end_time - self.start_time
    #         minutes = int(total_time // 60)
    #         seconds = total_time % 60
    #         # print(f'Time taken to complete PDF and KMZ download is {minutes} minutes and {seconds:.2f} seconds')
    #         print(f'Time taken to complete PDF and KMZ download is {minutes} minutes and {round(seconds)} seconds')
    #         time.sleep(2)
    #         pdf_icon = WebDriverWait(self.driver, 30).until(
    #             EC.presence_of_element_located(LensLocators.PDF_ICON)
    #         )
    #         print('[INFO] : PDF ICON DISPLAYED')
    #
    #         kmz_icon = WebDriverWait(self.driver, 30).until(
    #             EC.presence_of_element_located(LensLocators.KMZ_ICON)
    #         )
    #         print('[INFO] : KMZ ICON DISPLAYED')
    #
    #         close = WebDriverWait(self.driver, 20).until(
    #             EC.element_to_be_clickable(LensLocators.TOAST_CLOSE)
    #         )
    #         close.click()
    #         print('[INFO]: CLICKED ON TOAST CLOSE..')
    #
    #
    #         return True
    #
    #     except Exception as e:
    #         print(f'[ERROR] : FAILED TO CAPTURE TOAST MESSAGE: {e}')
    #         return False


    def export_aoi(self):
        try:
            time.sleep(4)
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
            actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
            print("[INFO]: right click happend...")

            # selecting ISP footprint
            # Hover and click "ISP Footprint Report"

            service = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_BUTTON)
            )
            actions.move_to_element(service).click().perform()
            time.sleep(2)

            export_aoi_report = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_AOI)
            )
            actions.move_to_element(export_aoi_report).click().perform()

            submit_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.EXPORT_AOI_SUBMIT)
            )
            submit_btn.click()
            print('[INFO]: Export AOI submit clicked')
            time.sleep(2)

            return True

        except Exception as e:
            print('[ERROR] : FAILED TO CLICK ON AOI SUBMIT')
            return False




    def add_to_sales_territory(self):
        time.sleep(4)
        wait = WebDriverWait(self.driver, 20)
        #
        actions = ActionChains(self.driver)

        map_element = wait.until(EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Map']")))
        actions.context_click(map_element).perform()
        #
        # mark_area_of_interest = wait.until(
        #     EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Mark as Area of Interest']")))
        # mark_area_of_interest.click()
        #
        time.sleep(2)
        #
        # actions.context_click(map_element).perform()
        #
        # time.sleep(10)

        click_on_add_to_sales_territory = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Add to Sales Territory']")))
        click_on_add_to_sales_territory.click()

        input_name = self.driver.find_element(By.XPATH, "//input[@id='sales-name']")
        print("entered name")
        input_name.clear()
        input_name.send_keys("Sales territory entry created through automation")
        time.sleep(2)

        submit_sales_entry = wait.until(EC.presence_of_element_located((By.XPATH, "// button[ @ id = 'add_sales_submit_btn']")))
        submit_sales_entry.click()

        confirm_sales_entry = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='jconfirm-buttons']/button[@class='btn btn-orange']"))
        )
        confirm_sales_entry.click()

        return True

    def map_view_sales_territory(self):
        wait = WebDriverWait(self.driver, 20)
        time.sleep(10)

        sales_territory_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='sales_territory_action_control']")))
        sales_territory_icon.click()
        time.sleep(5)

        search_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='saleTerritory-search']")))
        print("1")
        search_input.send_keys("Sales territory entry created through automation")

        map_view_icon = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//td[contains(.,'Sales territory entry created through automation')]/..//td[4]//i[@title='Map view']")))  #"(//i[contains(@class,'fa fa-map sales-table-maps') and @title='Map view'])"
        # time.sleep(5)
        map_view_icon.click()

        return True

    def edit_sales_territory(self):
        time.sleep(10)
        wait = WebDriverWait(self.driver, 20)

        search_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='saleTerritory-search']")))
        search_input.clear()
        time.sleep(4)
        search_input.send_keys("Sales territory entry created through automation")

        edit_icon = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//td[contains(.,'Sales territory entry created through automation')]/..//td[4]//i[@title='Edit']")))
        print("1")
        edit_icon.click()

        time.sleep(5)
        dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@id='select2-users-dropdown-container']")))
        dropdown.click()

        time.sleep(7)
        option_xpath = "//li[contains(@class, 'select2-results__option') and text()='hotwire admin']"
        option = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        option.click()
        time.sleep(5)

        submit_button_for_edit = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='submit-saleTerritory-btn']")))
        submit_button_for_edit.click()

        time.sleep(10)

        close_sales = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@id='saleTerritory_cancel_button']")))
        close_sales.click()

        return True

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


            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
            print("[INFO]: right click happend...")

            # right click on selecting geology export
            # actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
            # print("[INFO]: right click happend successfully...")

            export_aoi = WebDriverWait(self.driver, 50).until(
                EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_AOI)
            )
            actions.move_to_element(export_aoi).click().perform()
            print("[INFO]: CLICKED ON EXPORT AOI SUCCESSFULLY")
            time.sleep(1)

            export_aoi_submit = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(Context_Menu_Locators.EXPORT_AOI_SUBMIT)
            )
            export_aoi_submit.click()
            print("[INFO] : CLICKED ON EXPORT AOI SUBMIT")
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO RIGHT CLICK AND SELECT EXPORT AOI')
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
            print(f'INFO : {msg}')

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
            text3 = f"The Network distribution {report_name} has been completed . Please click the map button to view it."

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


    # def network_distribution(self):
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
    #         actions = ActionChains(self.driver)
    #         actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
    #         print("[INFO]: right click happend...")
    #
    #         # right click on selecting geology export
    #         # actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
    #         # print("[INFO]: right click happend successfully...")
    #
    #         export_aoi = WebDriverWait(self.driver, 50).until(
    #             EC.visibility_of_element_located(Context_Menu_Locators.NETWORK_DISTRIBUTION)
    #         )
    #         actions.move_to_element(export_aoi).click().perform()
    #         print("[INFO]: CLICKED ON NETWORK DISTRIBUTION SUCCESSFULLY")
    #         time.sleep(1)
    #
    #         value = WebDriverWait(self.driver, 30).until(
    #             EC.visibility_of_element_located(Context_Menu_Locators.ND_PROJECT_NAME)
    #         )
    #         report_name = value.get_attribute("value")
    #         with open("report_name.txt", "w", encoding="utf-8") as f:
    #             f.write(report_name)
    #
    #         description_message = WebDriverWait(self.driver, 30).until(
    #             EC.visibility_of_element_located(Context_Menu_Locators.NETWORK_DISTRIBUTION_DESCRIPTION)
    #         )
    #         msg = f'{report_name} generated successfully by AUTOMATION'
    #         description_message.send_keys(msg)
    #         print("[INFO]: DESCRIPTION ADDED INTO TEXT_AREA..")
    #         time.sleep(3)
    #
    #         nd_submit = WebDriverWait(self.driver, 30).until(
    #             EC.element_to_be_clickable(Context_Menu_Locators.NETWORK_DISTRIBUTION_SUBMIT)
    #         )
    #         nd_submit.click()
    #         # self.start_time = time.time()
    #         print("[INFO]: CLICKED ON SUBMIT BUTTON")
    #         time.sleep(2)
    #         print(self.report_name)
    #         return True
    #
    #     except Exception as e:
    #         print('[ERROR]: FAILED TO CLICK ON SUBMIT BUTTON')
    #         return False


