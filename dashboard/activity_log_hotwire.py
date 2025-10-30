import random

from prettytable import PrettyTable
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# import ..config.config
from ..config.config_customer import *
from ..config.assertion_config import *
from ..locators.lens_locators import LensLocators
from ..locators.dashboard_locators import DashboardLocators
from ..locators.right_icon_locators import RightIconLocators
from ..pages.map_page import MapPage
from ..pages.common import BasePage
from datetime import datetime
from selenium.webdriver.support.select import Select
import time,os
from ..config.config import *
import time



# #old code

class DashboardTaskHotwire(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.served = None

    def activityloghotwire(self):
        try:
            parent_handle = self.driver.current_window_handle

            # Step 1: Click on user link
            user_link = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(DashboardLocators.USERLINK)
            )
            user_link.click()
            time.sleep(2)

            # Step 2: Click on dashboard link
            dashboard_tracker = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(DashboardLocators.DASHBOARD)
            )
            dashboard_tracker.click()
            print('[INFO]: CLICKED ON DASHBOARD')

            # Step 3: Switch to new tab(s)
            for handle in self.driver.window_handles:
                if handle != parent_handle:
                    self.driver.switch_to.window(handle)
                    time.sleep(2)

                    try:

                        # Step 4: Click on Activity Log
                        act_log = WebDriverWait(self.driver, 20).until(
                            EC.element_to_be_clickable(RightIconLocators.ACTIVITY_LOG)
                        )
                        act_log.click()
                        print('[INFO]: CLICKED ON ACTIVITY LOG')
                        time.sleep(10)

                        # Step 5: Select VCTI from org dropdown
                        # dropdown_element = WebDriverWait(self.driver, 10).until(
                        #     EC.presence_of_element_located(RightIconLocators.ACTIVITY_LOG_DD)
                        # )
                        # Select(dropdown_element).select_by_visible_text("VCTI")
                        # print('[INFO]: SELECTED VCTI ORGANIZATION')
                        # time.sleep(2)
                        #
                        # # Step 6: Select USER from All Users dropdown
                        # dropdown_element1 = WebDriverWait(self.driver, 10).until(
                        #     EC.presence_of_element_located(RightIconLocators.ALL_USERS_DD)
                        # )
                        # Select(dropdown_element1).select_by_value(USERNAME)
                        # print(f'[INFO]: SELECTED USER --> {USERNAME}')
                        # time.sleep(2)

                        #scrolling down
                        # scrolling down to 'Next' link
                        xpath = "//a[.='Next'][1]"
                        next_button = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, xpath))
                        )
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_button)
                        print("[INFO]: SCROLLED TO 'Next' BUTTON")
                        time.sleep(2)

                        # # Step 8: Enter Username in footer field
                        username_footer_input = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable(RightIconLocators.FOOTER_USERNAME)
                        )
                        username_footer_input.clear()
                        username_footer_input.send_keys(HOTWIRE_USER)
                        print('[INFO]: ENTERED USERNAME IN FOOTER')

                        # Step 9: Enter Activity
                        activity_footer_input = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable(RightIconLocators.FOOTER_ACTIVITY)
                        )
                        activity_footer_input.clear()
                        activity_footer_input.send_keys(ACTIVITY_ACTIVITY_HOTWIRE)
                        print('[INFO]: ENTERED ACTIVITY IN FOOTER')
                        time.sleep(15)

                        #step 10 : enter area
                        area = WebDriverWait(self.driver,20).until(
                            EC.element_to_be_clickable(DashboardLocators.ACTIVITY_AREA)
                        )
                        assert area is not None, "[ASSERT FAIL] AREA FIELD NOT FOUND"
                        area.clear()
                        area.send_keys(ACTIVITY_HOTWIRE_AREA)
                        print(f'[INFO] : ENTERED ACTIVITY AREA --> {ACTIVITY_HOTWIRE_AREA}')
                        time.sleep(2)

                        #step11 :

                        # activity_service_provider = WebDriverWait(self.driver,20).until(
                        #     EC.element_to_be_clickable(DashBoard_Locators.ACTIVITY_SERVICE_PROVIDER)
                        # )
                        # self.driver.execute_script(
                        #     "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", activity_service_provider)
                        # # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", activity_service_provider)
                        # # activity_service_provider.clear()
                        # activity_service_provider.send_keys(ACTIVITY_SERVICE_PROVIDER)
                        # print(f'[INFO] : ENTERED ACTIVITY SERVICE PROVIDER --> {ACTIVITY_SERVICE_PROVIDER}')
                        # time.sleep(1)
                        #
                        # #step 12: entereing status
                        status = WebDriverWait(self.driver,20).until(
                            EC.element_to_be_clickable(DashboardLocators.ACTIVITY_SUCCESS)
                        )
                        assert status is not None, "[ASSERT FAIL] STATUS FIELD NOT FOUND"
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", status)
                        # status.clear()
                        status.send_keys(LOGS_STATUS)
                        print(f'[INFO] : ENTERED ACTIVITY STATUS --> {LOGS_STATUS}')
                        time.sleep(5)

                        #table
                        headers = ["Username", "Activity", "Area","Status", "Remarks","Date"]
                        rows = self.driver.find_elements(By.XPATH, "//table[@id='db-user-activity-table']//tbody//tr")
                        assert rows, "[ASSERT FAIL] NO ROWS FOUND IN ACTIVITY LOG TABLE"
                        table = PrettyTable()
                        table.field_names = headers
                        actual_usernames, actual_activities, actual_areas, actual_status = [], [], [], []

                        for row in rows[1:]:
                            cells = row.find_elements(By.TAG_NAME, "td")
                            if len(cells) >= 3:  # Avoid rows without enough cells
                                # Manually extract by index; fill missing ones if not available
                                username = cells[0].text.strip() if len(cells) > 0 else ""
                                activity = cells[1].text.strip() if len(cells) > 1 else ""
                                area = cells[2].text.strip() if len(cells) > 2 else ""
                                status = cells[4].text.strip() if len(cells) > 3 else ""
                                remarks = cells[5].text.strip() if len(cells) > 4 else ""
                                date = cells[6].text.strip() if len(cells) > 5 else ""
                                table.add_row([username, activity, area,status, remarks, date])

                                actual_usernames.append(username)
                                actual_activities.append(activity)
                                actual_areas.append(area)
                                actual_status.append(status)

                        print("\n[INFO] : Extracted Table:\n")
                        print(table)

                        assert any(HOTWIRE_USER.lower() in u.lower() for u in
                                   actual_usernames), "[ASSERT FAIL] USERNAME NOT FOUND IN TABLE"
                        assert any(ACTIVITY_ACTIVITY_HOTWIRE.lower() in a.lower() for a in
                                   actual_activities), "[ASSERT FAIL] ACTIVITY NOT FOUND"
                        assert any(
                            ACTIVITY_HOTWIRE_AREA.lower() in a.lower() for a in actual_areas), "[ASSERT FAIL] AREA NOT FOUND"
                        assert any(
                            LOGS_STATUS.lower() in s.lower() for s in actual_status), "[ASSERT FAIL] STATUS NOT FOUND"
                        print("[INFO]: ALL ENTERED VALUES SUCCESSFULLY VALIDATED IN TABLE")
                        return True
                    #
                    except Exception as e1:
                        print(f"[WARNING] Could not interact with tab {handle}: {e1}")

                    finally:
                        print(f'[INFO] CLOSING CHILD WINDOW : {handle}')
                        self.driver.close()
                        self.driver.switch_to.window(parent_handle)
                        print("[INFO]: RETURNED TO PARENT WINDOW")

            # Step 10: Return to Parent Window
            time.sleep(2)
            # self.driver.switch_to.window(parent_handle)
            # print("[INFO]: RETURNED TO PARENT WINDOW")
            return True

        except Exception as e:
            print(f"[ERROR] Failed in activitylog: {e}")
            return False


    def click_next_previous_page(self):
        try:
            next_page = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(DashboardLocators.ACTIVITY_NEXT)
            )
            next_page.click()
            print('[INFO] : CLICKED ON NEXT PAGE')
            time.sleep(1)
            previous_page = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(DashboardLocators.ACTIVITY_PREVIOUS)
            )
            previous_page.click()
            print('[INFO] : CLICKED ON PREVIOUS PAGE')
            time.sleep(1)
            page_number_click = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(DashboardLocators.ACTIVITY_PAGE_NUMBER)
            )
            page_number_click.click()
            print(f'[INFO] : CLICKED ON PAGE-NUMBER:{PAGES_NUMBER}')
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO CLICK ON NEXT,PREVIOUS PAGE')
            return False