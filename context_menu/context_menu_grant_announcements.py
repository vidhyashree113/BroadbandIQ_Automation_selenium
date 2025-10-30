# from traceback import print_tb
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
from ..pages.map_page import MapPage
from selenium.webdriver.support.select import Select
import traceback


class GrantAnnoncement(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def right_click_grant_annoucement(self):
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
            pole_owner = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.GRANT_ANNOUNCEMENT)
            )
            actions.move_to_element(pole_owner).click().perform()
            time.sleep(2)
            print("[INFO] : CLICKED ON GRANT ANNOUNCEMENT")
            return True

        except Exception as e:
            print(f'[ERROR] : GRANT ANNOUNCEMENT FAILED --> {e}')
            return False

    # def click_each_grant_section_get_data(self):
    #     sections = [
    #         (Context_Menu_Locators.GRANT_FEDERAL, "Federal"),
    #         (Context_Menu_Locators.GRANT_STATE, "State"),
    #         (Context_Menu_Locators.GRANT_COUNTY, "Counties"),
    #         (Context_Menu_Locators.GRANT_RFP, "RFP"),
    #         (Context_Menu_Locators.GRANT_VIDEOLINKS, "Video Links"),
    #     ]
    #
    #     all_passed = True
    #
    #     for locator, section_name in sections:
    #         try:
    #             print(f"\nSection: {section_name}")
    #
    #             xpath = locator[1]
    #             section_element = self.wait.until(EC.presence_of_element_located(locator))
    #
    #             # Check if already expanded
    #             try:
    #                 content_div = self.driver.find_element(By.XPATH, f"{xpath}/following-sibling::div")
    #                 is_displayed = content_div.is_displayed()
    #             except:
    #                 is_displayed = False
    #
    #             # Click only if not expanded
    #             if not is_displayed:
    #                 section_element.click()
    #                 print(f"Clicked on '{section_name}' to expand")
    #                 content_div = self.wait.until(
    #                     EC.presence_of_element_located((By.XPATH, f"{xpath}/following-sibling::div"))
    #                 )
    #                 time.sleep(1)
    #             else:
    #                 print(f"'{section_name}' already expanded")
    #
    #             # Try capturing table
    #             try:
    #                 table_element = content_div.find_element(By.TAG_NAME, "table")
    #                 headers = table_element.find_elements(By.XPATH, ".//thead/tr/th")
    #                 rows = table_element.find_elements(By.XPATH, ".//tbody/tr")
    #
    #                 pt = PrettyTable()
    #                 pt.field_names = [h.text.strip() for h in headers]
    #
    #                 for row in rows:
    #                     cells = row.find_elements(By.TAG_NAME, "td")
    #                     pt.add_row([cell.text.strip() for cell in cells])
    #
    #                 print(f"Table from '{section_name}':\n{pt}")
    #
    #             except Exception:
    #                 text = content_div.text.strip()
    #                 if text:
    #                     print(f"Text from '{section_name}':\n{text}")
    #                 else:
    #                     print(f"No table or text found in '{section_name}'")
    #
    #         except Exception as e:
    #             print(f"[ERROR] Failed to process section '{section_name}': {e}")
    #             all_passed = False
    #
    #     return all_passed

    def _expand_and_get_section_data(self, locator, section_name):
        try:
            print(f"\nSection: {section_name}")
            xpath = locator[1]
            section_element = WebDriverWait(self.driver,20).until(EC.presence_of_element_located(locator))

            # Check if already expanded
            try:
                content_div = self.driver.find_element(By.XPATH, f"{xpath}/following-sibling::div")
                is_displayed = content_div.is_displayed()
            except:
                is_displayed = False

            # Expand if needed
            if not is_displayed:
                section_element.click()
                print(f"Clicked on '{section_name}' to expand")
                content_div = WebDriverWait(self.driver,20).until(
                    EC.presence_of_element_located((By.XPATH, f"{xpath}/following-sibling::div"))
                )
                time.sleep(1)
            else:
                print(f"'{section_name}' already expanded")

            # Try capturing table or text
            try:
                table_element = content_div.find_element(By.TAG_NAME, "table")
                headers = table_element.find_elements(By.XPATH, ".//thead/tr/th")
                rows = table_element.find_elements(By.XPATH, ".//tbody/tr")

                pt = PrettyTable()
                pt.field_names = [h.text.strip() for h in headers]

                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    pt.add_row([cell.text.strip() for cell in cells])

                print(f"Table from '{section_name}':\n{pt}")
            except Exception:
                text = content_div.text.strip()
                if text:
                    print(f"Text from '{section_name}':\n{text}")
                else:
                    print(f"No table or text found in '{section_name}'")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to process section '{section_name}': {e}")
            return False

        # Public methods for each section

    def process_federal_section(self):
        return self._expand_and_get_section_data(Context_Menu_Locators.GRANT_FEDERAL, "Federal")

    def process_state_section(self):
        return self._expand_and_get_section_data(Context_Menu_Locators.GRANT_STATE, "State")

    def process_county_section(self):
        return self._expand_and_get_section_data(Context_Menu_Locators.GRANT_COUNTY, "Counties")

    def process_rfp_section(self):
        return self._expand_and_get_section_data(Context_Menu_Locators.GRANT_RFP, "RFP")

    def process_video_links_section(self):
        return self._expand_and_get_section_data(Context_Menu_Locators.GRANT_VIDEOLINKS, "Video Links")

    def run_all_grant_sections(self):
        self.right_click_grant_annoucement()
        self.process_federal_section()
        self.process_state_section()
        self.process_county_section()
        self.process_rfp_section()
        self.process_video_links_section()
        self.close_section()

    def close_section(self):
        try:
            close = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(Context_Menu_Locators.GRANT_CLOSE)
            )
            close.click()
            print('[INFO] CLICKED ON GRANT CLOSE')
            return True

        except Exception as e:
            print(f'[ERROR] GRANT CLOSE FAILED--> {e}')
            return False