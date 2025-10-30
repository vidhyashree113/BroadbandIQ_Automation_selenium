import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

from ..locators.context_menu_locators import Context_Menu_Locators
from ..locators.lens_locators import LensLocators
from ..config.config import *
from ..locators.right_icon_locators import RightIconLocators


class NetworkDistribution_Dialog_box:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)
        self.start_time = None
        self.end_time = None
        self.driver = driver
        self.report_name = ''

    def upload_any_aoi(self):
        try:
            print("[STEP] Opening Upload AOI Tool...")
            aoi_icon = self.wait.until(EC.element_to_be_clickable(RightIconLocators.UPLOAD_AOI_TOOL))
            aoi_icon.click()
#"C:\Users\nikitha.deshpande\Downloads\Area 10 1.kmz"
            file_path = os.path.abspath(os.path.expanduser("~/Downloads/Area 10 1.kmz"))
            print(f"[STEP] Uploading file from path: {file_path}")
            upload_input = self.wait.until(EC.presence_of_element_located(RightIconLocators.CHOOSE_FILE))
            upload_input.send_keys(file_path)
            time.sleep(5)

            submit_button = self.wait.until(EC.presence_of_element_located(RightIconLocators.SUBMIT_AOI))
            submit_button.click()
            print("[STEP] Submitted AOI upload.")
            time.sleep(5)


            actions = ActionChains(self.driver)
            map_element = self.wait.until(
                EC.presence_of_element_located(Context_Menu_Locators.MAP_CANVAS)
            )

            print("[STEP] Right clicking on the map to mark AOI...")
            actions.context_click(map_element).perform()
            mark_aoi = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Mark as Area of Interest']"))
            )
            mark_aoi.click()
            print("[STEP] Marked AOI.")
            time.sleep(10)

            print("[STEP] Right clicking again to select Network Distribution...")
            actions.context_click(map_element).perform()
            time.sleep(5)

            network_distribution_option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Network Distribution']"))
            )
            network_distribution_option.click()
            time.sleep(5)

            print("[SUCCESS] AOI upload and Network Distribution dialog opened successfully.")
            return True

        except Exception as e:
            print(f"[ERROR] Failed during AOI upload: {e}")
            return False

    def validate_cabinet_capacity_default(self):
        """Validate Cabinet Capacity field default value."""
        element = self.wait.until(EC.presence_of_element_located(RightIconLocators.CABINET_CAPACITY_FIELD))
        value = element.get_attribute("value")
        print(f"[ASSERT] Cabinet Capacity default: expected='{CABINET_CAPACITY}', actual='{value}'")
        return value == CABINET_CAPACITY

    def validate_flowerpot_capacity_default(self):
        """Validate Flowerpot Capacity field default value."""
        element = self.wait.until(EC.presence_of_element_located(RightIconLocators.FLOWERPOT_CAPACITY_FIELD))
        value = element.get_attribute("value")
        print(f"[ASSERT] Flowerpot Capacity default: expected='{FLOWERPOT_CAPACITY}', actual='{value}'")
        return value == FLOWERPOT_CAPACITY

    def validate_adjacent_locations_default(self):
        """Validate Adjacent Locations field default value."""
        element = self.wait.until(EC.presence_of_element_located(RightIconLocators.ADJACENT_LOCATIONS_FIELD))
        value = element.get_attribute("value")
        print(f"[ASSERT] Adjacent Locations default: expected='{ADJACENT_LOCATIONS}', actual='{value}'")
        return value == ADJACENT_LOCATIONS

    def validate_dropline_length_default(self):
        """Validate Dropline Length dropdown default value."""
        element = self.wait.until(EC.presence_of_element_located(RightIconLocators.DROPLINE_LENGTH_DROPDOWN))
        value = element.get_attribute("value")
        print(f"[ASSERT] Dropline Length default: expected='{DROPLINE_LENGTH}', actual='{value}'")
        return value == DROPLINE_LENGTH

    def validate_add_description(self):
        try:
            element = self.wait.until(EC.presence_of_element_located(RightIconLocators.DESCRIPTION))

            # 🔹 Capture ND_PROJECT_NAME before clicking submit
            project_name_field = self.wait.until(
                EC.presence_of_element_located(Context_Menu_Locators.ND_PROJECT_NAME)
            )
            report_name = project_name_field.get_attribute("value")

            with open("report_name1.txt", "w", encoding="utf-8") as f:
                f.write(report_name)

            msg = f"{report_name} generated successfully by AUTOMATION"
            element.send_keys(msg)

            submit_net = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@id='network_dist_submit_btn']"))
            )
            submit_net.click()
            print(f"[STEP] Clicked submit on Network Distribution with project: {report_name}")

            return True
        except Exception as e:
            print(f"[ERROR] Failed to add description: {e}")
            return False

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

    def validate_toast_messages(self):
        """Validate toast messages after submit is clicked."""
        try:
            self.start_time = time.time()
            with open("report_name1.txt", "r", encoding="utf-8") as f:
                report_name = f.read().strip()
            print(f"[INFO] Project name for toast validation: '{report_name}'")

            text2 = f"The request for the Network Distribution Path has been successfully submitted. Notification will be sent once the path is generated and ready."
            text3 = f"The Network distribution {report_name} has been completed . Please click the map button to view it."

            print(f"[WAITING] : Toast Accepted --> {text2}")
            # if not self.wait_for_toast_text(text2, timeout=30):
            #     print(f"[ERROR] Toast not found for: {text2}")
            #     return False
            # print("[SUCCESS]: First toast verified.")

            print(f"[WAITING]: Toast: Completed --> {text3}")
            if not self.wait_for_toast_text(text3, timeout=30):
                print(f"[ERROR] Toast not found for: {text3}")
                return False
            print("[SUCCESS]: Second toast verified.")

            close = self.wait.until(
                EC.element_to_be_clickable(Context_Menu_Locators.TOAST_CLOSE)
            )
            close.click()
            print('[INFO]: CLICKED ON TOAST CLOSE..')

            self.end_time = time.time()
            total_time = self.end_time - self.start_time
            minutes = int(total_time // 60)
            seconds = total_time % 60
            print(f'Time taken to complete ND path is {minutes} minutes and {round(seconds)} seconds')
            return True

        except Exception as e:
            print(f'[ERROR] : FAILED TO VALIDATE TOAST MESSAGE: {e}')
            return False

    def verify_cancel_without_desc(self):
        try:
            print(f"[INFO] Clicking on Submit without adding description")
            submit_net = self.wait.until(
                EC.element_to_be_clickable(RightIconLocators.NETWORK_DIS_SUBMIT)
            )
            submit_net.click()

            click_cancel = self.wait.until(
                EC.element_to_be_clickable(RightIconLocators.CANCEL_NETWORK_SUBMIT)
            )
            click_cancel.click()
            print("[STEP] Clicked submit without description on Network Distribution.")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to click on submit: {e}")
            return False

    def locations_upload(self):
        try:
            #"C:\Users\nikitha.deshpande\Downloads\Area 10_1.geojson"
            file_path = os.path.abspath(os.path.expanduser("~/Downloads/Area 10_1.geojson"))
            print(f"Uploading locations geojson from path: {file_path}")
            upload_input = self.wait.until(EC.presence_of_element_located(RightIconLocators.UPLOAD_GEOJSON))
            upload_input.send_keys(file_path)

            return True
        except Exception as e:
            print(f"Location file upload failed")
            return False

    def add_olt(self):
        try:
            print("[STEP] Clicking on OLT option...")
            olt_btn = self.wait.until(EC.element_to_be_clickable(RightIconLocators.OLT))
            olt_btn.click()
            print("[STEP] OLT option clicked.")

            lat_input = self.wait.until(
                EC.presence_of_element_located(RightIconLocators.OLT_LATITUDE_PATH)
            )
            lat_input.clear()
            lat_input.send_keys(OLT_LATITUDE)
            print(f"[ASSERT] Entered Latitude: expected='{OLT_LATITUDE}'")

            lon_input = self.wait.until(
                EC.presence_of_element_located(RightIconLocators.OLT_LONGITUDE_PATH)
            )
            lon_input.clear()
            lon_input.send_keys(OLT_LONGITUDE)
            print(f"[ASSERT] Entered Longitude: expected='{OLT_LONGITUDE}'")

            print("[SUCCESS] OLT details entered successfully.")
            return True

        except Exception as e:
            print(f"[ERROR] Failed while adding OLT: {e}")
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

            network_description = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(Context_Menu_Locators.NETWORK_DISTRIBUTION_DESCRIPTION))

            network_description.send_keys(msg)
            print(f'INFO : Description Message entered --> {msg}')

            network_description_submit = WebDriverWait(self.driver, 30).until(
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
            # if not self.wait_for_toast_text(text2, timeout=90):
            #     print(f"[ERROR] Toast not found for: {text2}")
            #     return False
            # print("[SUCCESS]: All toasts received and verified.")

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









