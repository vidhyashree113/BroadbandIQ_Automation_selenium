from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..config.config import *
from ..config.assertion_config import *
from ..locators.right_icon_locators import RightIconLocators
from ..locators.dashboard_locators import DashboardLocators
from ..locators.lens_locators import LensLocators
from ..pages.map_page import MapPage
from ..pages.common import BasePage
from ..resources.login_page import LoginPage
from selenium.webdriver.support.select import Select
from prettytable import PrettyTable
from datetime import datetime
import time, os


class Logs(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def click_logs(self):
        try:
            user_link = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(DashboardLocators.USERLINK)
            )
            user_link.click()
            time.sleep(2)

            logs = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.LOGS)
            )
            logs.click()
            print("[INFO] : CLICKED ON LOGS")
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO CLICK ON LOGS')
            return False

    def click_next_previous_page(self):
        try:
            next_page = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(DashboardLocators.LOGS_NEXT_BUTTON)
            )
            next_page.click()
            print('[INFO] : CLICKED ON NEXT PAGE')
            time.sleep(1)
            previous_page = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(DashboardLocators.LOGS_PREVIOUS_BUTTON)
            )
            previous_page.click()
            print('[INFO] : CLICKED ON PREVIOUS PAGE')
            time.sleep(1)
            page_number_click = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(DashboardLocators.LOGS_PAGE_NUMBER)
            )
            page_number_click.click()
            print(f'[INFO] : CLICKED ON PAGE-NUMBER:{PAGES_NUMBER}')
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO CLICK ON NEXT,PREVIOUS PAGE')
            return False

    def logs_search_county(self):
        try:
            # Step 1: Enter Activity
            activity = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_ACTIVITY_LOGS)
            )
            activity.clear()
            activity.send_keys(LOGS_ACTIVITY)
            print(f'[INFO] : ENTERED ACTIVITY --> {LOGS_ACTIVITY}')

            # Step 2: Enter Region
            time.sleep(1)
            region = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_REGION)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region)
            region.send_keys(LOGS_REGION)
            print(f'[INFO] : ENTERED REGION --> {LOGS_REGION}')

            # Step 3: Enter Region Type
            region_type = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_REGION_TYPE)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region_type)
            region_type.send_keys(LOGS_REGION_TYPE)
            print(f'[INFO] : ENTERED REGION TYPE --> {LOGS_REGION_TYPE}')
            time.sleep(4)

            # Step 4: Extract table headers
            headers = ["Search", "Region", "Region Type", "Status", "Remarks", "Date"]

            # header_elements = self.driver.find_elements(By.XPATH,
            #                                             "//table[@class='table table-striped table-hover dataTable']//thead//th")
            # headers = [header.text.strip() for header in header_elements]

            # Step 5: Extract table rows
            rows = self.driver.find_elements(By.XPATH, "//table[@id='user-activity-table']//tbody//tr")

            # Step 6: Create PrettyTable and print
            table = PrettyTable()
            table.field_names = headers
            all_region = []

            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 3:  # Avoid rows without enough cells
                    # Manually extract by index; fill missing ones if not available
                    search = cells[0].text.strip() if len(cells) > 0 else ""
                    region = cells[1].text.strip() if len(cells) > 1 else ""
                    region_type = cells[2].text.strip() if len(cells) > 2 else ""
                    status = cells[6].text.strip() if len(cells) > 3 else ""
                    remarks = cells[7].text.strip() if len(cells) > 4 else ""
                    date = cells[8].text.strip() if len(cells) > 5 else ""
                    table.add_row([search, region, region_type, status, remarks, date])

            # for i in all_region:
            #     print(f'Expected : {LOGS_REGION} | Actual : {i}')
            assert LOGS_REGION_LABEL == region,'Not found region'
            print(f'Expected : {LOGS_REGION_LABEL} | ACTUAL : {region}')
            print("\n[INFO] : Extracted Table:\n")
            print(table)
            assert all(region.lower() in LOGS_REGION.lower() for address in
                       all_region), f"[ERROR] Not all statuses are 'Success': {all_region}"
            return True


        except Exception as e:
            print(f"[ERROR] : FAILED TO ENTER LOG DETAILS - {str(e)}")
            assert False




    def search_log_co_ordinates(self):
        try:

            activity = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_ACTIVITY_LOGS)
            )
            activity.clear()
            time.sleep(1)

            region = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_REGION)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region)
            region.clear()

            region_type = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_REGION_TYPE)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region_type)
            region_type.clear()

            address = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_ADDRESS)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", address)
            address.clear()

            #step5 : entering co-ordinates
            co_ordinates = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_COORDINATES)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", co_ordinates)
            co_ordinates.clear()
            co_ordinates.send_keys(CO_ORDINATES)
            print(f'[INFO] : ENTERED CO-ORDINATES --> {CO_ORDINATES}')
            time.sleep(4)

            headers = ["Search", "Region", "Region Type","Address","Co_ordinates","Status", "Remarks", "Date"]
            rows = self.driver.find_elements(By.XPATH, "//table[@id='user-activity-table']//tbody//tr")

            # Step 6: Create PrettyTable and print
            table = PrettyTable()
            table.field_names = headers
            all_co_ordinates = []

            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 3:  # Avoid rows without enough cells
                    # Manually extract by index; fill missing ones if not available
                    search = cells[0].text.strip() if len(cells) > 0 else ""
                    region = cells[1].text.strip() if len(cells) > 1 else ""
                    region_type = cells[2].text.strip() if len(cells) > 2 else ""
                    address = cells[3].text.strip() if len(cells)>3 else ""
                    coordinates = cells[4].text.strip() if len(cells)>4 else ''
                    status = cells[6].text.strip() if len(cells) > 3 else ""
                    remarks = cells[7].text.strip() if len(cells) > 4 else ""
                    date = cells[8].text.strip() if len(cells) > 5 else ""
                    table.add_row([search, region, region_type, address,coordinates,status, remarks, date])


            # assert LOGS_CO_ORDINATES_LABEL == cooridnates,'CO_ORDINATES NOT FOUND'
            # print(f'EXPECTED : {LOGS_CO_ORDINATES_LABEL} | ACTUAL : {co_ordinates}')
            assert LOGS_CO_ORDINATES_LABEL.lower() in coordinates.lower(), f"CO_ORDINATES NOT FOUND | EXPECTED: {LOGS_CO_ORDINATES_LABEL} | FOUND: {cooridnates}"
            print(f'EXPECTED : {LOGS_CO_ORDINATES_LABEL} | ACTUAL : {coordinates}')
            print("\n[INFO] : Extracted Table:\n")
            print(table)
            assert all(coordinates.lower() in CO_ORDINATES.lower() for coordinates in
                       all_co_ordinates), f"[ERROR] Not all statuses are 'Success': {all_co_ordinates}"

            return True

        except Exception as e:
            print(f"[ERROR] : FAILED TO ENTER LOG CO_ORDINATES DETAILS - {str(e)}")
            assert False


    def search_log_address(self):
        try:
            activity = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_ACTIVITY_LOGS)
            )
            activity.clear()
            time.sleep(1)

            region = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_REGION)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region)
            region.clear()

            region_type = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_REGION_TYPE)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region_type)
            region_type.clear()

            # step4 : entering address
            address = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_ADDRESS)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", address)
            address.clear()
            address.send_keys(LOGS_ADDRESS)
            print(f'[INFO] : ENTERED ADDRESS --> {LOGS_ADDRESS}')
            time.sleep(4)
            headers = ["Search", "Region", "Region Type", "Address", "Co_ordinates", "Status", "Remarks", "Date"]
            rows = self.driver.find_elements(By.XPATH, "//table[@id='user-activity-table']//tbody//tr")

            # Step 6: Create PrettyTable and print
            table = PrettyTable()
            table.field_names = headers
            all_address = []

            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 3:  # Avoid rows without enough cells
                    # Manually extract by index; fill missing ones if not available
                    search = cells[0].text.strip() if len(cells) > 0 else ""
                    region = cells[1].text.strip() if len(cells) > 1 else ""
                    region_type = cells[2].text.strip() if len(cells) > 2 else ""
                    address = cells[3].text.strip() if len(cells) > 3 else ""
                    cooridnates = cells[4].text.strip() if len(cells) > 4 else ''
                    status = cells[6].text.strip() if len(cells) > 3 else ""
                    remarks = cells[7].text.strip() if len(cells) > 4 else ""
                    date = cells[8].text.strip() if len(cells) > 5 else ""
                    table.add_row([search, region, region_type, address,cooridnates,status, remarks, date])

            assert LOGS_ADDRESS_LABEL.capitalize() in address, 'ADDRESS NOT FOUND'
            print(f'EXPECTED : {LOGS_ADDRESS_LABEL} | ACTUAL : {address}')
            print("\n[INFO] : Extracted Table:\n")
            print(table)
            assert all(address.lower() in LOGS_ADDRESS.lower() for address in all_address), f"[ERROR] Not all statuses are 'Success': {all_address}"
            return True

        except Exception as e:
            print(f"[ERROR] : FAILED TO ENTER LOG ADDRESS DETAILS - {str(e)}")
            assert False

    def search_log_success(self):
        try:
            activity = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_ACTIVITY_LOGS)
            )
            activity.clear()
            time.sleep(1)

            region = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_REGION)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region)
            region.clear()

            region_type = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_REGION_TYPE)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region_type)
            region_type.clear()

            address = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_ADDRESS)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", address)
            address.clear()

            co_ordinates = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_COORDINATES)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", co_ordinates)
            co_ordinates.clear()

            #step6 : entering status

            status = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_STATUS)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", status)
            status.clear()
            status.send_keys(LOGS_STATUS)
            print(f'[INFO] : ENTERED STATUS --> {LOGS_STATUS}')
            time.sleep(4)
            headers = ["Search", "Region", "Region Type", "Address", "Co_ordinates", "Status", "Remarks", "Date"]
            rows = self.driver.find_elements(By.XPATH, "//table[@id='user-activity-table']//tbody//tr")

        # Step 6: Create PrettyTable and print
            table = PrettyTable()
            table.field_names = headers
            all_status = []

            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 3:  # Avoid rows without enough cells
                    # Manually extract by index; fill missing ones if not available
                    search = cells[0].text.strip() if len(cells) > 0 else ""
                    region = cells[1].text.strip() if len(cells) > 1 else ""
                    region_type = cells[2].text.strip() if len(cells) > 2 else ""
                    address = cells[3].text.strip() if len(cells) > 3 else ""
                    cooridnates = cells[4].text.strip() if len(cells) > 4 else ''
                    status = cells[6].text.strip() if len(cells) > 3 else ""
                    remarks = cells[7].text.strip() if len(cells) > 4 else ""
                    date = cells[8].text.strip() if len(cells) > 5 else ""
                    table.add_row([search, region, region_type, address, cooridnates, status, remarks, date])

                    # if LOGS_STATUS.lower() in status.lower():
                    #     status_match_found = True


            # assert status.lower() in LOGS_STATUS, f'Expected {LOGS_STATUS} but got {status}'
            assert LOGS_STATUS_SUCCESS_LABEL.lower() == status.lower(), 'SUCCESS STATUS NOT FOUND'
            print(f'EXPECTED : {LOGS_STATUS_SUCCESS_LABEL} | ACTUAL : {status}')
            print("\n[INFO] : Extracted Table:\n")

            assert all(status.lower() == LOGS_STATUS.lower() for status in all_status), f"[ERROR] Not all statuses are 'Success': {all_status}"
            return True

        except Exception as e:
            print(f"[ERROR] : FAILED TO ENTER LOG ADDRESS DETAILS - {str(e)}")
            assert False


    def search_log_status_failure(self):
        try:
            activity = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_ACTIVITY_LOGS)
            )
            activity.clear()
            time.sleep(1)

            region = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_REGION)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region)
            region.clear()

            region_type = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_REGION_TYPE)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region_type)
            region_type.clear()

            address = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_ADDRESS)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", address)
            address.clear()

            co_ordinates = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_COORDINATES)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", co_ordinates)
            co_ordinates.clear()

            #step6 : entering status

            status = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_STATUS)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", status)
            status.clear()
            status.send_keys(LOGS_STATUS_FAILURE)
            print(f'[INFO] : ENTERED STATUS --> {LOGS_STATUS_FAILURE}')
            time.sleep(4)
            headers = ["Search", "Region", "Region Type", "Address", "Co_ordinates", "Status", "Remarks", "Date"]
            rows = self.driver.find_elements(By.XPATH, "//table[@id='user-activity-table']//tbody//tr")

        # Step 6: Create PrettyTable and print
            table = PrettyTable()
            table.field_names = headers
            all_status = []

            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 3:  # Avoid rows without enough cells
                    # Manually extract by index; fill missing ones if not available
                    search = cells[0].text.strip() if len(cells) > 0 else ""
                    region = cells[1].text.strip() if len(cells) > 1 else ""
                    region_type = cells[2].text.strip() if len(cells) > 2 else ""
                    address = cells[3].text.strip() if len(cells) > 3 else ""
                    cooridnates = cells[4].text.strip() if len(cells) > 4 else ''
                    status = cells[6].text.strip() if len(cells) > 3 else ""
                    remarks = cells[7].text.strip() if len(cells) > 4 else ""
                    date = cells[8].text.strip() if len(cells) > 5 else ""
                    table.add_row([search, region, region_type, address, cooridnates, status, remarks, date])

                    # if LOGS_STATUS.lower() in status.lower():
                    #     status_match_found = True


            # assert status.lower() in LOGS_STATUS, f'Expected {LOGS_STATUS} but got {status}'
            # for i in all_status:
            #     print(f'Expected : {LOGS_STATUS_FAILURE} | Actual : {i}')
            # # print(table)
            assert LOGS_STATUS_FAILURE_LABELS.lower()== status.lower(), 'FAILURE STATUS NOT FOUND'
            print(f'EXPECTED : {LOGS_STATUS_FAILURE_LABELS} | ACTUAL : {status}')

            print("\n[INFO] : Extracted Table:\n")
            print(table)
            assert all(status.lower() == LOGS_STATUS.lower() for status in all_status), f"[ERROR] Not all statuses are 'Success': {all_status}"
            return True

        except Exception as e:
            print(f"[ERROR] : FAILED TO ENTER LOG ADDRESS DETAILS - {str(e)}")
            assert False

    def close_logs(self):
        try:
            close = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(DashboardLocators.FOOTER_LOGS_CLOSE)
            )
            close.click()
            print('[INFO] : CLICKED ON CLOSE BUTTON')
            return True
        except Exception as e:
            print('[ERROR] : FAILED TO CLICK ON CLOSE BUTTON')
            return False

##################################################
# def footer_logs(self):
#     try:
#
#         #step-1: --> entering activity
#         activity = WebDriverWait(self.driver,20).until(
#             EC.element_to_be_clickable(DashBoard_Locators.FOOTER_ACTIVITY_LOGS)
#         )
#         activity.clear()
#         activity.send_keys(LOGS_ACTIVITY)
#         print(f'[INFO] : ENTERED ACTIVITY --> {LOGS_ACTIVITY}')
#
#         #step-2 : entering region
#         time.sleep(1)
#         region = WebDriverWait(self.driver,20).until(
#             EC.element_to_be_clickable(DashBoard_Locators.FOOTER_LOGS_REGION)
#         )
#         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region)
#
#         # region.clear()
#         region.send_keys(LOGS_REGION)
#         print(f'[INFO] : ENTERED REGION --> {LOGS_REGION}')
#
#         #step-3 : entering region type
#         region_type = WebDriverWait(self.driver,20).until(
#             EC.element_to_be_clickable(DashBoard_Locators.FOOTER_LOGS_REGION_TYPE)
#         )
#         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region_type)
#         # region_type.clear()
#         region_type.send_keys(LOGS_REGION_TYPE)
#         print(f'[INFO] : ENTERED REGION TYPE --> {LOGS_REGION_TYPE}')
#         time.sleep(1)
#
#         #step4 : entering address
#         address = WebDriverWait(self.driver,20).until(
#             EC.element_to_be_clickable(DashBoard_Locators.FOOTER_LOGS_ADDRESS)
#         )
#         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", address)
#         address.clear()
#         address.send_keys(LOGS_ADDRESS)
#         print(f'[INFO] : ENTERED ADDRESS --> {LOGS_ADDRESS}')
#         time.sleep(1)
#
#         #step5 : entering co-ordinates
#         co_ordinates = WebDriverWait(self.driver,20).until(
#             EC.element_to_be_clickable(DashBoard_Locators.FOOTER_LOGS_COORDINATES)
#         )
#         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", co_ordinates)
#         co_ordinates.clear()
#         co_ordinates.send_keys(CO_ORDINATES)
#         print(f'[INFO] : ENTERED CO-ORDINATES --> {CO_ORDINATES}')
#         time.sleep(1)
#
#         #step6 : entering status
#
#         status = WebDriverWait(self.driver,20).until(
#             EC.element_to_be_clickable(DashBoard_Locators.FOOTER_LOGS_STATUS)
#         )
#         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", status)
#         status.clear()
#         status.send_keys(LOGS_STATUS)
#         print(f'[INFO] : ENTERED STATUS --> {LOGS_STATUS}')
#         return True
#
#     except Exception as e:
#         print(f'[ERROR] : LOGS FOOTER FAILED : {e}')
#         return False