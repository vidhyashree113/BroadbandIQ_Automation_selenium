import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from ..locators.right_icon_locators import RightIconLocators
from ..locators.lens_locators import LensLocators
from ..config.config import *

class NetworkDistribution_LargeAOI:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)
        self.report_name = ''

    def wait_for_toast_text(self, expected_text, timeout=60, poll_frequency=1):
        by, value = LensLocators.NOTIFICATION_ALERT
        print("[DEBUG] Waiting for toast text...")
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

    def details_net_dis_report(self):
        try:
            value = WebDriverWait(self.driver, 40).until(
                EC.visibility_of_element_located(LensLocators.PROJECT_NAME)
            )
            self.report_name = value.get_attribute("value").strip()
            if not self.report_name:
                raise ValueError("[ERROR] PROJECT_NAME input is empty!")

            print(f"[INFO] Captured project name: '{self.report_name}'")

            directory = os.path.abspath("network_distribution_reports")
            os.makedirs(directory, exist_ok=True)

            report_path = os.path.join(directory, "report_name.txt")
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(self.report_name)

            print(f"[INFO] Report name written to file: {report_path}")
            return True

        except Exception as e:
            print(f'[ERROR]: FAILED TO CAPTURE REPORT NAME: {e}')
            return False

    def capturing_toast_message(self):
        try:
            print("[DEBUG] Starting toast capture...")

            if not self.report_name:
                raise ValueError("Report name is empty; cannot proceed with toast check.")

            toast_text = f"An error occurred while processing the Network Distribution request for {self.report_name}. Please try again later or reach out to support for assistance."
            print(f"[WAITING]: Toast: {toast_text}")

            if not self.wait_for_toast_text(toast_text, timeout=600):
                print(f"[ERROR] Toast not found for: {toast_text}")
                return False

            print("[SUCCESS]: Toast received and verified.")
            return True

        except Exception as e:
            print(f'[ERROR]: FAILED TO CAPTURE TOAST MESSAGE: {e}')
            return False

    def upload_file_and_trigger_network_distribution(self):
        try:
            print("[STEP] Opening Upload AOI Tool...")
            aoi_icon = self.wait.until(EC.element_to_be_clickable(RightIconLocators.UPLOAD_AOI_TOOL))
            aoi_icon.click()

            file_path = os.path.abspath(os.path.expanduser("~/Downloads/Ector_county.geojson"))
            print(f"[STEP] Uploading file from path: {file_path}")
            upload_input = self.wait.until(EC.presence_of_element_located(RightIconLocators.CHOOSE_FILE))
            upload_input.send_keys(file_path)
            time.sleep(20)

            submit_button = self.wait.until(EC.presence_of_element_located(RightIconLocators.SUBMIT_AOI))
            submit_button.click()
            print("[STEP] Submitted AOI upload.")
            time.sleep(10)

            actions = ActionChains(self.driver)
            map_element = self.wait.until(EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Map']")))

            print("[STEP] Right clicking on the map to mark AOI...")
            actions.context_click(map_element).perform()
            mark_aoi = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Mark as Area of Interest']")))
            mark_aoi.click()
            print("[STEP] Marked AOI.")
            time.sleep(10)

            print("[STEP] Right clicking again to select Network Distribution...")
            actions.context_click(map_element).perform()
            time.sleep(5)

            network_distribution_option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Network Distribution']")))
            network_distribution_option.click()
            time.sleep(5)

            if not self.details_net_dis_report():
                return False

            print("[STEP] Submitting Network Distribution request...")
            submit_net = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[@id='network_dist_submit_btn']")))
            submit_net.click()
            print("[STEP] Clicked submit on Network Distribution.")

            confirm_network_dis = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Confirm']"))
            )
            confirm_network_dis.click()

            print("[INFO] Waiting for Toast...")
            if not self.capturing_toast_message():
                return False

            print("[SUCCESS] Network Distribution flow completed.")
            return True

        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            return False
