#zipcode_Code
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

class UploadKmz_Muncipal(BasePage):
    def __init__(self, driver):
        super().__init__(driver)


    def muncipal_upload_aoi(self):

        try:
            wait = WebDriverWait(self.driver, 20)

            aoi_icon = wait.until(EC.element_to_be_clickable(RightIconLocators.UPLOAD_AOI_TOOL))
            aoi_icon.click()

            file_name = "Smith River-Gasquet CCD - Del Norte County, CA.kmz"  # or .kmz
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