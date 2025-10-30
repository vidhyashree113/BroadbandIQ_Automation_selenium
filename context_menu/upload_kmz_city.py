

#city_Code

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

class UploadKmz_City(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def get_kmz_path(self):
        downloads = os.path.expanduser("~\\Downloads")
        today = datetime.date.today()
        pdf_files = [os.path.join(downloads, f) for f in os.listdir(downloads) if
                     f.startswith("Splendora ciy") and f.endswith(".kmz")]
        kmz_files_today = [f for f in pdf_files if datetime.date.fromtimestamp(os.path.getmtime(f)) == today]
        if not kmz_files_today:
            return None, "❌ No KMZ file found."
        return max(kmz_files_today, key=os.path.getmtime), None

    def aoi(self):

        try:
            wait = WebDriverWait(self.driver, 20)

            aoi_icon = wait.until(EC.element_to_be_clickable(RightIconLocators.UPLOAD_AOI_TOOL))
            aoi_icon.click()

            file_name = "Splendora city, TX.kmz"  # or .kmz
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

    # def upload_AOI_city(self):
    #     try:
    #
    #         # time.sleep(5)
    #         canvas = WebDriverWait(self.driver, 30).until(
    #             EC.presence_of_element_located((By.CLASS_NAME, "mapboxgl-canvas"))
    #         )
    #         self.driver.execute_script("arguments[0].scrollIntoView(true);", canvas)
    #         time.sleep(3)
    #
    #         width = canvas.size['width']
    #         height = canvas.size['height']
    #         center_x = width // 2
    #         center_y = height // 2
    #         offset_x = 40  # Shift slightly to the right of center
    #         offset_y = 10
    #         actions = ActionChains(self.driver)
    #         actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
    #         print("[INFO]: right click happend...")
    #
    #         # selecting MARK AREA OF INTREST
    #         aoi = WebDriverWait(self.driver, 30).until(
    #             EC.element_to_be_clickable(Context_Menu_Locators.MARK_AOI)
    #         )
    #         actions.move_to_element(aoi).click().perform()
    #         print("[INFO]: CLICKED ON MARK AOI SUCCESSFULLY")
    #         time.sleep(2)
    #         return True
    #     except Exception as e:
    #         print(e)
    #         print('[ERROR] : FAILED TO RIGHT CLICK AND SELECT MARK AREA OF INTEREST')
    #         return False



