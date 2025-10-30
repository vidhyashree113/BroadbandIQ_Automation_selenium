import os
import time
# import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from ..config.config import *
from ..pages.common import BasePage
from ..bbiq_lens.locations import LocationLens
from ..locators.right_icon_locators import RightIconLocators
from ..locators.context_menu_locators import Context_Menu_Locators

class EXPORT_AOI(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # self.location_lens = LocationLens(driver)

    def export_aoi_kmz(self):
        wait = WebDriverWait(self.driver, 20)
        actions = ActionChains(self.driver)

        aoi_icon = wait.until(EC.element_to_be_clickable(RightIconLocators.UPLOAD_AOI_TOOL))
        aoi_icon.click()

        file_path = os.path.abspath(os.path.expanduser("~/Downloads/Ector_county.geojson"))

        upload_input = wait.until(EC.presence_of_element_located(RightIconLocators.CHOOSE_FILE))
        upload_input.send_keys(file_path)

        time.sleep(20)
        submit_button = wait.until(EC.presence_of_element_located(RightIconLocators.SUBMIT_AOI))
        submit_button.click()

        map_element = wait.until(EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Map']")))
        actions.context_click(map_element).perform()

        mark_area_of_interest = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Mark as Area of Interest']")))
        mark_area_of_interest.click()

        time.sleep(15)


        actions.context_click(map_element).perform()

        export_aoi = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Export Area of Interest']")))
        export_aoi.click()


        submit_export_aoi_kmz = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='add_aoi_submit_btn']")))
        submit_export_aoi_kmz.click()

        time.sleep(5)

    def export_aoi_kmz1(self):
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

        # wait = WebDriverWait(self.driver, 20)
        # actions = ActionChains(self.driver)
        #
        # map_element = wait.until(EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Map']")))
        # actions.context_click(map_element).perform()
        #
        # # mark_area_of_interest = wait.until(
        # #     EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Mark as Area of Interest']")))
        # # mark_area_of_interest.click()
        #
        # time.sleep(15)
        #
        # actions.context_click(map_element).perform()
        #
        # export_button = WebDriverWait(self.driver, 30).until(
        #     EC.visibility_of_element_located(Context_Menu_Locators.EXPORT_BUTTON)
        # )
        # actions.move_to_element(export_button).click().perform()
        # print("[INFO]: Export button clicked from context menu.")
        # time.sleep(2)
        #
        # # actions.context_click(export_button).perform()
        #
        # export_aoi = wait.until(
        #     EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Export Area of Interest']")))
        # export_aoi.click()
        #
        # time.sleep(5)
        #
        # submit_export_aoi_kmz = wait.until(
        #     EC.presence_of_element_located((By.XPATH, "//button[@id='add_aoi_submit_btn']")))
        # submit_export_aoi_kmz.click()
        #
        # time.sleep(10)


    def export_aoi_csv(self):
        wait = WebDriverWait(self.driver, 20)
        actions = ActionChains(self.driver)

        aoi_icon = wait.until(EC.element_to_be_clickable(RightIconLocators.UPLOAD_AOI_TOOL))
        aoi_icon.click()

        file_path = os.path.abspath(os.path.expanduser("~/Downloads/Ector_county.geojson"))

        upload_input = wait.until(EC.presence_of_element_located(RightIconLocators.CHOOSE_FILE))
        upload_input.send_keys(file_path)

        time.sleep(20)
        submit_button = wait.until(EC.presence_of_element_located(RightIconLocators.SUBMIT_AOI))
        submit_button.click()

        time.sleep(3)
        error_text = self.driver.find_elements(*Context_Menu_Locators.UPLOAD_STATUS_VALUE)

        if error_text:
            error_value = error_text[0].text.strip()  # exatrcting error text and removing space at leading and trailing side
            assert not error_value, f"Upload Submit failed : {error_value}"

        map_element = wait.until(EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Map']")))
        actions.context_click(map_element).perform()

        mark_area_of_interest = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Mark as Area of Interest']")))
        mark_area_of_interest.click()

        time.sleep(15)

        # self.location_lens.click_locations_lens()
        #
        # time.sleep(15)

        actions.context_click(map_element).perform()

        export_aoi = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Export Area of Interest']")))
        export_aoi.click()


        submit_export_aoi_csv = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='add_aoi_submit_btn']")))
        submit_export_aoi_csv.click()

        time.sleep(5)
