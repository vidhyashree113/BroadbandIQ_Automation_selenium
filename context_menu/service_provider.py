# from traceback import print_tb
import os

import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..locators.right_icon_locators import RightIconLocators
import time
from ..locators.lens_locators import LensLocators
from ..locators.context_menu_locators import Context_Menu_Locators
from ..config.config import *
from ..pages.common import BasePage
from ..locators.right_icon_locators import RightIconLocators
from ..pages.map_page import MapPage
from selenium.webdriver.support.select import Select
import traceback


class ServiceProvider1(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    _wireline_xpath = "//tbody[@id='sp_competation_wire_line_body']//tr" #
    _fwa_header_xpath = "//tr[@id='sp_competation_fwa_header']//span[@class='tree-toggle glyphicon glyphicon-chevron-right']"
    _fwa_xpath = "//tr[@id='sp_competation_fwa_header']/following-sibling::tr//td[@id='sp-action-toggles']//span[@class='switch-slider round']/../../.."

    _satellite_header_xpath = "//tr[@id='sp_competation_satelite_header']//span[contains(@class,'tree-toggle')]"
    _satellite_xpath = "//tbody[@id='sp_competation_satelite_body']//tr[td[@id='sp-action-toggles']]"

    def right_click_service_provider(self):
        try:
            print("[INFO]: Right-clicked on the red-colored area (estimated position).")


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
                EC.visibility_of_element_located(Context_Menu_Locators.SERVICE_PROVIDER)
            )
            actions.move_to_element(service).click().perform()
            time.sleep(2)
            print("[INFO] : CLICKED ON SERVICE PROVIDER")

            self.wait_for_element(Context_Menu_Locators.SERVICE_PROVIDER_ELEMENT,timeout_value,poll_frequency_value)
            return True

        except Exception as e:
            print(f'[ERROR] : SERVICE PROVIDER FLOW FAILED --> {e}')
            return False

    # def upload_county_geojson(self):
    #     wait = WebDriverWait(self.driver, 20)
    #
    #     aoi_icon = wait.until(EC.element_to_be_clickable(UPLOAD_AOI_TOOL))
    #     aoi_icon.click()
    #
    #     file_path = os.path.abspath(os.path.expanduser("~/Downloads/Ector_county.geojson"))
    #
    #     upload_input = wait.until(EC.presence_of_element_located(CHOOSE_FILE))
    #     upload_input.send_keys(file_path)
    #
    #     time.sleep(20)
    #     submit_button = wait.until(EC.presence_of_element_located(SUBMIT_AOI))
    #     submit_button.click()
    #
    #     time.sleep(10)
    #
    #     actions = ActionChains(self.driver)
    #
    #     map_element = wait.until(EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Map']")))
    #     actions.context_click(map_element).perform()
    #
    #     mark_area_of_interest = wait.until(
    #         EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Mark as Area of Interest']")))
    #     mark_area_of_interest.click()
    #
    #     time.sleep(10)
    #
    #     actions.context_click(map_element).perform()
    #
    #     time.sleep(10)
    #     click_on_service_provider = wait.until(
    #         EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Service Providers']")))
    #     click_on_service_provider.click()

    # def click_service_provider(self):
    #     wait = WebDriverWait(self.driver, 20)
    #
    #     actions = ActionChains(self.driver)
    #
    #     map_element = wait.until(EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Map']")))
    #     actions.context_click(map_element).perform()
    #
    #     click_on_service_provider = wait.until(
    #         EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Service Providers']")))
    #     click_on_service_provider.click()

    def _get_toggle_rows(self, xpath, section_name="Unknown", skip_count=0):
        rows = self.driver.find_elements(By.XPATH, xpath)
        interactable = []

        print(f"\nChecking {len(rows)} raw toggle rows from XPath for [{section_name}]...\n")
        for i, row in enumerate(rows, 1):
            if i <= skip_count:
                print(f"Skipping non-toggle row #{i} in [{section_name}]")
                continue

            try:
                tds = row.find_elements(By.TAG_NAME, "td")
                if len(tds) < 6:
                    raise ValueError("Expected at least 6 <td> elements")

                provider = tds[1].text.strip()
                tech = tds[2].text.strip()
                toggle = tds[5].find_element(By.XPATH, ".//span[@class='switch-slider round']")

                print(f"Row #{i}: Provider = '{provider}', Technology = '{tech}'")
                if provider and tech:
                    interactable.append((row, toggle))
            except Exception as e:
                print(f"Skipping row #{i} due to error: {e}")
                continue

        return interactable

    def _expand_fwa_section(self):
        try:
            fwa_header = self.driver.find_element(By.XPATH, self._fwa_header_xpath)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", fwa_header)
            time.sleep(2)

            #Click to expand FWA section if collapsible
            self.driver.execute_script("arguments[0].click();", fwa_header)
              # give time for rows to load
            print("Expanded FWA section.")
            time.sleep(3)
        except Exception as e:
            pytest.fail(f"Failed to expand FWA section: {e}")

    def _expand_section(self, header_xpath, section_name):
        try:
            header = self.driver.find_element(By.XPATH, header_xpath)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", header)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", header)
            print(f"Expanded {section_name} section.")
            time.sleep(3)
        except Exception as e:
            pytest.fail(f"Failed to expand {section_name} section: {e}")


    def _toggle_rows(self, rows, action, section_name):
        print(f"{'Turning OFF' if action == 'off' else 'Turning ON'} {len(rows)} toggles in [{section_name}]")

        for idx, (row, toggle_btn) in enumerate(rows, 1):
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", row)
                time.sleep(1)

                cells = row.find_elements(By.TAG_NAME, "td")
                provider = cells[1].text.strip()  # td[2]
                tech = cells[2].text.strip()  # td[3]

                self.driver.execute_script("arguments[0].click();", toggle_btn)
                time.sleep(1)

                print(
                    f"{'✅' if action == 'on' else '🛑'} [{section_name}] Turned {action.upper()}: Provider = '{provider}', Technology = '{tech}'")
            except Exception as e:
                pytest.fail(f"❌ Failed to toggle [{section_name}] row #{idx}: {e}")

    def toggle_all(self):
        # Step 1: Wireline (skip first 2 rows)
        wireline_rows = self._get_toggle_rows(self._wireline_xpath, section_name="Wireline", skip_count=2)
        self._toggle_rows(wireline_rows, "on", "Wireline")

        # Step 2: FWA (no skipping)
        self._expand_fwa_section()
        fwa_rows = self._get_toggle_rows(self._fwa_xpath, section_name="FWA")  # No skip_count
        self._toggle_rows(fwa_rows, "on", "FWA")

        self._expand_section(self._satellite_header_xpath, "Satellite")
        satellite_rows = self._get_toggle_rows(self._satellite_xpath, section_name="Satellite")
        self._toggle_rows(satellite_rows, "on", "Satellite")

        # Total valid toggles
        all_rows = wireline_rows + fwa_rows
        print(f"Total valid toggles found: {len(all_rows)}")

        # Step 3: Turn all OFF
        self._toggle_rows(all_rows, "off", "All Sections")


    def download_csv(self):
        try:
            csv = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.EXPORT_CSV)
            )
            csv.click()
            print('[INFO] : CLICK ON EXPORT CSV BUTTON')

            time.sleep(1)

            csv_submit = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.EXPORT_CSV_SUBMIT)
            )
            csv_submit.click()
            print('[INFO] : CLICKED ON EXPORT CSV SUBMIT BUTTON')
            time.sleep(10)

            return True

        except Exception as e:
            print(f'[ERROR] : FAILED TO EXPORT CSV --> {e}')
            return False

    def service_provider_close(self):
        wait = WebDriverWait(self.driver, 20)

        service_provider_close = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(Context_Menu_Locators.SERVICE_PROVIDER_CLOSE)
        )
        service_provider_close.click()


    # _wireline_xpath = "//tbody[@id='sp_competation_wire_line_body']//tr" #
    # _fwa_header_xpath = "//tr[@id='sp_competation_fwa_header']//span[@class='tree-toggle glyphicon glyphicon-chevron-right']"
    # _fwa_xpath = "//tr[@id='sp_competation_fwa_header']/following-sibling::tr//td[@id='sp-action-toggles']//span[@class='switch-slider round']/../../.."
    #
    #
    # def right_click_service_provider(self):
    #     try:
    #         print("[INFO]: Right-clicked on the red-colored area (estimated position).")
    #
    #
    #         canvas = WebDriverWait(self.driver,30).until(
    #             EC.element_to_be_clickable((By.CLASS_NAME, "mapboxgl-canvas"))
    #         )
    #         width = canvas.size['width']
    #         height = canvas.size['height']
    #         center_x = width // 2
    #         center_y = height // 2
    #
    #         offset_x = center_x + 30
    #         offset_y = center_y
    #         actions = ActionChains(self.driver)
    #         actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
    #         print("[INFO]: right click happend...")
    #
    #         # selecting ISP footprint
    #         # Hover and click "ISP Footprint Report"
    #         service = WebDriverWait(self.driver, 30).until(
    #             EC.visibility_of_element_located(LensLocators.SERVICE_PROVIDER)
    #         )
    #         actions.move_to_element(service).click().perform()
    #         time.sleep(2)
    #         print("[INFO] : CLICKED ON SERVICE PROVIDER")
    #         return True
    #
    #     except Exception as e:
    #         print(f'[ERROR] : SERVICE PROVIDER FLOW FAILED --> {e}')
    #
    def upload_county_geojson(self):
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

        actions = ActionChains(self.driver)

        map_element = wait.until(EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Map']")))
        actions.context_click(map_element).perform()

        mark_area_of_interest = wait.until(
            EC.element_to_be_clickable(Context_Menu_Locators.SERVICE_PROVIDER_MARK_AOI))
        mark_area_of_interest.click()

        time.sleep(10)

        actions.context_click(map_element).perform()

        time.sleep(20)

        click_on_service_provider = wait.until(
            EC.element_to_be_clickable(Context_Menu_Locators.SERVICE_PROVIDER))
        click_on_service_provider.click()
    #
    # def _get_toggle_rows(self, xpath, section_name="Unknown", skip_count=0):
    #     rows = self.driver.find_elements(By.XPATH, xpath)
    #     interactable = []
    #
    #     print(f"\nChecking {len(rows)} raw toggle rows from XPath for [{section_name}]...\n")
    #     for i, row in enumerate(rows, 1):
    #         if i <= skip_count:
    #             print(f"Skipping non-toggle row #{i} in [{section_name}]")
    #             continue
    #
    #         try:
    #             tds = row.find_elements(By.TAG_NAME, "td")
    #             if len(tds) < 6:
    #                 raise ValueError("Expected at least 6 <td> elements")
    #
    #             provider = tds[1].text.strip()
    #             tech = tds[2].text.strip()
    #             toggle = tds[5].find_element(Context_Menu_Locators.slider_button)
    #
    #             print(f"Row #{i}: Provider = '{provider}', Technology = '{tech}'")
    #             if provider and tech:
    #                 interactable.append((row, toggle))
    #         except Exception as e:
    #             print(f"Skipping row #{i} due to error: {e}")
    #             continue
    #
    #     return interactable
    #
    # def _expand_fwa_section(self):
    #     try:
    #         fwa_header = self.driver.find_element(By.XPATH, self._fwa_header_xpath)
    #         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", fwa_header)
    #         time.sleep(2)
    #
    #         #Click to expand FWA section if collapsible
    #         self.driver.execute_script("arguments[0].click();", fwa_header)
    #           # give time for rows to load
    #         print("Expanded FWA section.")
    #         time.sleep(3)
    #     except Exception as e:
    #         pytest.fail(f"Failed to expand FWA section: {e}")
    #
    # def _toggle_rows(self, rows, action, section_name):
    #     print(f"{'Turning OFF' if action == 'off' else 'Turning ON'} {len(rows)} toggles in [{section_name}]")
    #
    #     for idx, (row, toggle_btn) in enumerate(rows, 1):
    #         try:
    #             self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", row)
    #             time.sleep(1)
    #
    #             cells = row.find_elements(By.TAG_NAME, "td")
    #             provider = cells[1].text.strip()  # td[2]
    #             tech = cells[2].text.strip()  # td[3]
    #
    #             self.driver.execute_script("arguments[0].click();", toggle_btn)
    #             time.sleep(1)
    #
    #             print(
    #                 f"{'✅' if action == 'on' else '🛑'} [{section_name}] Turned {action.upper()}: Provider = '{provider}', Technology = '{tech}'")
    #         except Exception as e:
    #             pytest.fail(f"❌ Failed to toggle [{section_name}] row #{idx}: {e}")
    #
    # def toggle_all(self):
    #     # Step 1: Wireline (skip first 2 rows)
    #     wireline_rows = self._get_toggle_rows(self._wireline_xpath, section_name="Wireline", skip_count=2)
    #     self._toggle_rows(wireline_rows, "on", "Wireline")
    #
    #     # Step 2: FWA (no skipping)
    #     self._expand_fwa_section()
    #     fwa_rows = self._get_toggle_rows(self._fwa_xpath, section_name="FWA")  # No skip_count
    #     self._toggle_rows(fwa_rows, "on", "FWA")
    #
    #     # Total valid toggles
    #     all_rows = wireline_rows + fwa_rows
    #     print(f"Total valid toggles found: {len(all_rows)}")
    #
    #     # Step 3: Turn all OFF
    #     self._toggle_rows(all_rows, "off", "All Sections")
    #
    #
    # def download_csv(self):
    #     try:
    #         csv = WebDriverWait(self.driver,30).until(
    #             EC.element_to_be_clickable(LensLocators.EXPORT_CSV)
    #         )
    #         csv.click()
    #         print('[INFO] : CLICK ON EXPORT CSV BUTTON')
    #
    #         time.sleep(1)
    #
    #         csv_submit = WebDriverWait(self.driver,30).until(
    #             EC.element_to_be_clickable(LensLocators.EXPORT_CSV_SUBMIT)
    #         )
    #         csv_submit.click()
    #         print('[INFO] : CLICKED ON EXPORT CSV SUBMIT BUTTON')
    #         time.sleep(10)
    #
    #         #closing service provider window
    #         close = WebDriverWait(self.driver,20).until(
    #             EC.element_to_be_clickable(LensLocators.SERVICE_PROVIDER_CLOSE)
    #         )
    #         close.click()
    #         print('[INFO] : CLICKED ON SERVICE PROVIDER CLOSE BUTTON')
    #         return True
    #
    #     except Exception as e:
    #         print(f'[ERROR] : FAILED TO EXPORT CSV --> {e}')
    #         return False




###############################################################################
"""
toggle on ---> download ---> toggle off

def toggle_and_download_csv(self):
    # Step 1: Toggle ON
    wireline_rows = self._get_toggle_rows(self._wireline_xpath, section_name="Wireline", skip_count=2)
    self._toggle_rows(wireline_rows, "on", "Wireline")

    self._expand_fwa_section()
    fwa_rows = self._get_toggle_rows(self._fwa_xpath, section_name="FWA")  # No skip count
    self._toggle_rows(fwa_rows, "on", "FWA")

    all_rows = wireline_rows + fwa_rows
    print(f"🧮 Total toggles turned ON: {len(all_rows)}")

    # Step 2: Export CSV
    self._download_csv_report()

    # Step 3: Toggle OFF
    self._toggle_rows(all_rows, "off", "All Sections")


test method

def test_toggle_and_download_csv(setup):
    try:
        service_provider = setup  # Assuming 'setup' fixture returns page object
        service_provider.toggle_and_download_csv()
    except Exception as e:
        pytest.fail(f"❌ Test failed during toggle + CSV export flow: {e}")
"""