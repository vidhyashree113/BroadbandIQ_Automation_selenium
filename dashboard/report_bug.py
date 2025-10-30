from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..config.config import *
from ..config.assertion_config import *
from ..locators.right_icon_locators import RightIconLocators
from ..locators.login_locators import LoginPageLocators
from ..pages.map_page import MapPage
from ..pages.common import BasePage
from selenium.webdriver.support.select import Select
from prettytable import PrettyTable
from datetime import datetime
import time,os


class Report_bug(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.served = None
        self.driver = driver

    def report_bug(self):

        try:

            #cliciking on report bug icon
            bug_icon = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable(RightIconLocators.REPORT_BUG_ICON)
            )

            bug_icon.click()
            time.sleep(3)
            print('[INFO] : CLICKED ON REPORT BUG ICON')


        #entering the bug title

            time.sleep(3)
            bug_title = WebDriverWait(self.driver,30).until(
            EC.presence_of_element_located(RightIconLocators.BUG_TITLE)
            )

            bug_title.send_keys(RightIconLocators.BUG_NAME)
            time.sleep(3)
            print('[INFO]: ENTERED BUG TITLE')



    #entering bug descripton

            time.sleep(3)
            bug_description = WebDriverWait(self.driver,30).until(
                EC.presence_of_element_located(RightIconLocators.BUG_DESCRIPTION)
            )
            bug_description.send_keys("Automated bug")
            time.sleep(3)
            print('[INFO] : ENTERED BUG DESCRITION')

    #click on submit
            bug_submit = WebDriverWait(self.driver,30).until(
            EC.element_to_be_clickable(RightIconLocators.BUG_SUBMIT)
            )

            bug_submit.click()
            print('[INFO} : CLICKED ON SUBMIT')
            time.sleep(10)
            return True


        except Exception as e:
            print('[ERROR] : FAILED..')
            return False


    def search_bug_tracker(self):

        try:

            #cliciking on bug tracker
            user_link = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable(LoginPageLocators.USER_LINK)
            )

            user_link.click()
            time.sleep(2)
            bug_tracker = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable(LoginPageLocators.BUG_TRACKER)
            )
            bug_tracker.click()
            print('[INFO] : CLICKED ON BUG TRACKER')

            #searching bug using title
            bug_search = WebDriverWait(self.driver,30).until(
                EC.presence_of_element_located(RightIconLocators.BUG_SEARCH)
            )
            bug_search.send_keys(RightIconLocators.BUG_NAME)
            print('[INFO] : SEARCHED BUG NAME')
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO SEARCH')
            return False

    def view_screenshot(self):

        try:
            time.sleep(3)
            search_screenshot = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable(RightIconLocators.BUG_SCREENSHOT)
            )
            search_screenshot.click()
            time.sleep(3)
            WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable((By.XPATH,"(//div[@class='text-right']//button[.='Close'])[1]"))
            ).click()
            print('[INFO] : SCREENSHOT DISPLAYED')
            return True
        except Exception as e:
            print('[ERROR]: FAILED TO CLICK ON SCREENSHOT')
            return False

    def view_preview(self):

        try:
            time.sleep(3)
            search_screenshot = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable(RightIconLocators.BUG_PREVIEW)
            )
            search_screenshot.click()
            print('[INFO] : SCREENSHOT PREVIEW DISPLAYED')
            preview_close = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable((By.XPATH,"(//div[@class='text-right']//button[.='Close'])[3]"))
            )
            preview_close.click()
            print("[INFO] : CLOSED ON PREVIEW CLOSE")
            time.sleep(3)

            close_button = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable((By.XPATH,"(//button[@id='cls-bug-btn'])[3]"))
            )
            close_button.click()
            print("[INFO]: CLICKED ON CLOSE BUTTON")
            return True
        except Exception as e:
            print('[ERROR]: FAILED TO CLICK ON SCREENSHOT PREVIEW')
            return False

    def bug_tracker_extract(self):
        try:
            parent_handle = self.driver.current_window_handle

            # Step 1: Click on user link
            user_link = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LoginPageLocators.USER_LINK)
            )
            user_link.click()
            time.sleep(2)

            # Step 2: Click on dashboard link
            dashboard_tracker = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LoginPageLocators.DASHBOARD)
            )
            dashboard_tracker.click()
            print('[INFO]: CLICKED ON DASHBOARD')

            # Step 3: Switch to new tab(s)
            for handle in self.driver.window_handles:
                if handle != parent_handle:
                    self.driver.switch_to.window(handle)
                    time.sleep(2)

                    try:
                        # Step 4: Click on Bug report
                        act_log = WebDriverWait(self.driver, 20).until(
                            EC.element_to_be_clickable(RightIconLocators.BUG_REPORT)
                        )
                        act_log.click()
                        print('[INFO]: CLICKED ON BUG REPORT')
                        time.sleep(3)

                        # Step 5: Select VCTI from org dropdown
                        dropdown_element = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(RightIconLocators.BUG_REPORT_DD)
                        )
                        dd_element = Select(dropdown_element)
                        dd_element.select_by_visible_text("VCTI")
                        print('[INFO]: SELECTED VCTI ORGANIZATION')
                        time.sleep(2)

                        # Step 6: Select user
                        dropdown_element1 = WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located(RightIconLocators.BUG_REPORT_USERS_DD)
                        )
                        dd_element_users = Select(dropdown_element1)
                        dd_element_users.select_by_value(USERNAME)
                        print(f'[INFO]: SELECTED USER --> {USERNAME}')
                        time.sleep(2)

                    # try:
                        # Step 7: Wait for and extract activity log table data
                        WebDriverWait(self.driver, 10).until(
                            EC.visibility_of_element_located(
                                (By.XPATH, "//table[@id='bugTable']/tbody/tr[1]/td[1]")
                            )
                        )
                        rows = self.driver.find_elements(By.XPATH, "//table[@id='bugTable']/tbody/tr")
                        all_data = []

                        for row in rows:
                            cells = row.find_elements(By.TAG_NAME, "td")
                            if len(cells) >= 6:
                                entry = {
                                    "Title": cells[0].get_attribute("innerText").strip(),
                                    "Assignee": cells[1].get_attribute("innerText").strip(),
                                    "Reporter": cells[2].get_attribute("innerText").strip(),
                                    "Status": cells[3].get_attribute("innerText").strip(),
                                    "Assigned Date": cells[4].get_attribute("innerText").strip(),
                                    "Resolved Date": cells[5].get_attribute("innerText").strip()
                                }
                                all_data.append(entry)

                        print("[INFO]: EXTRACTED BUG REPORT DATA")

                        # Create and populate PrettyTable
                        table = PrettyTable()
                        table.field_names = ["Title", "Assignee", "Reporter", "Status", "Assigned Date",
                                             "Resolved Date"]

                        for record in all_data:
                            table.add_row([
                                record["Title"],
                                record["Assignee"],
                                record["Reporter"],
                                record["Status"],
                                record["Assigned Date"],
                                record["Resolved Date"]
                            ])

                        print(table)  # Pretty print in tabular format

                    except Exception as e1:
                        print(f"[WARNING] Could not interact with tab {handle}: {e1}")


            #old code
            #             # Step 7: Wait for and extract activity log table data
            #             WebDriverWait(self.driver, 10).until(
            #                 EC.visibility_of_element_located(
            #                     (By.XPATH, "//table[@id='bugTable']/tbody/tr[1]/td[1]")
            #                 )
            #             )
            #             rows = self.driver.find_elements(By.XPATH, "//table[@id='bugTable']/tbody/tr")
            #             all_data = []
            #
            #             for row in rows:
            #                 cells = row.find_elements(By.TAG_NAME, "td")
            #                 if len(cells) >= 6:
            #                     entry = {
            #                         "Title": cells[0].get_attribute("innerText").strip(),
            #                         "Assignee": cells[1].get_attribute("innerText").strip(),
            #                         "Reporter": cells[2].get_attribute("innerText").strip(),
            #                         "Status": cells[3].get_attribute("innerText").strip(),
            #                         "Assigned Date": cells[4].get_attribute("innerText").strip(),
            #                         "Resolved Date": cells[5].get_attribute("innerText").strip()
            #                     }
            #                     all_data.append(entry)
            #
            #             print("[INFO]: EXTRACTED BUG REPORT DATA")
            #             for record in all_data:
            #                 print(record)
            #
            #         except Exception as e1:
            #             print(f"[WARNING] Could not interact with tab {handle}: {e1}")
            #
            # Final Step: Return to parent window
            time.sleep(2)
            self.driver.switch_to.window(parent_handle)
            print("[INFO]: RETURNED TO PARENT WINDOW")

            return True

        except Exception as e:
            print(f"[ERROR] Failed in bug_tracker: {e}")
            return False

    # def bug_tracker(self):   #old code
    #     try:
    #         parent_handle = self.driver.current_window_handle
    #
    #         # Step 1: Click on user link
    #         user_link = WebDriverWait(self.driver, 30).until(
    #             EC.element_to_be_clickable(LoginPageLocators.USER_LINK)
    #         )
    #         user_link.click()
    #         time.sleep(2)
    #
    #         # Step 2: Click on dashboard link
    #         dashboard_tracker = WebDriverWait(self.driver, 30).until(
    #             EC.element_to_be_clickable(LoginPageLocators.DASHBOARD)
    #         )
    #         dashboard_tracker.click()
    #         print('[INFO]: CLICKED ON DASHBOARD')
    #
    #         # Step 3: Switch to new tab(s)
    #         for handle in self.driver.window_handles:
    #             if handle != parent_handle:
    #                 self.driver.switch_to.window(handle)
    #                 time.sleep(2)
    #
    #                 try:
    #                     # Step 4: Click on Bug report
    #                     act_log = WebDriverWait(self.driver, 20).until(
    #                         EC.element_to_be_clickable(RightIconLocators.BUG_REPORT)
    #                     )
    #                     act_log.click()
    #                     print('[INFO]: CLICKED ON BUG REPORT')
    #                     time.sleep(3)
    #
    #                     # Step 5: Select VCTI from org dropdown
    #                     dropdown_element = WebDriverWait(self.driver, 10).until(
    #                         EC.presence_of_element_located(RightIconLocators.BUG_REPORT_DD)
    #                     )
    #                     dd_element = Select(dropdown_element)
    #                     dd_element.select_by_visible_text("VCTI")
    #                     print('[INFO]: SELECTED VCTI ORGANIZATION')
    #                     time.sleep(2)
    #
    #                     #step-6: Selecting users
    #                     dropdown_element1 = WebDriverWait(self.driver,20).until(
    #                         EC.presence_of_element_located(RightIconLocators.BUG_REPORT_USERS_DD)
    #                     )
    #                     dd_element_users = Select(dropdown_element1)
    #                     dd_element_users.select_by_value(USERNAME)
    #                     print(f'[INFO]: SELECTED USER --> {USERNAME}')
    #                     time.sleep(2)
    #
    #
    #                 except Exception as e1:
    #                     print(f"[WARNING] Could not interact with tab {handle}: {e1}")
    #
    #         # Step 10: Return to Parent Window
    #         # time.sleep(2)
    #         # self.driver.switch_to.window(parent_handle)
    #         # print("[INFO]: RETURNED TO PARENT WINDOW")
    #
    #         return True
    #
    #     except Exception as e:
    #         print(f"[ERROR] Failed in activitylog: {e}")
    #         return False

    # from selenium.webdriver.common.by import By
    # from selenium.webdriver.support.ui import WebDriverWait
    # from selenium.webdriver.support import expected_conditions as EC
    #
    # import time
    # from selenium.webdriver.common.by import By
    # from selenium.webdriver.support.ui import WebDriverWait
    # from selenium.webdriver.support import expected_conditions as EC
    #
    # def extract_activity_log_table_data(self, parent_handle):
    #     try:
    #         # Wait for the first cell in the first row to be visible
    #         WebDriverWait(self.driver, 10).until(
    #             EC.visibility_of_element_located((By.XPATH, "//table[@id='bugTable']/tbody/tr[1]/td[1]"))
    #         )
    #
    #         rows = self.driver.find_elements(By.XPATH, "//table[@id='bugTable']/tbody/tr")
    #         all_data = []
    #
    #         for row in rows:
    #             cells = row.find_elements(By.TAG_NAME, "td")
    #             if len(cells) >= 6:
    #                 entry = {
    #                     "Title": cells[0].get_attribute("innerText").strip(),
    #                     "Assignee": cells[1].get_attribute("innerText").strip(),
    #                     "Reporter": cells[2].get_attribute("innerText").strip(),
    #                     "Status": cells[3].get_attribute("innerText").strip(),
    #                     "Assigned Date": cells[4].get_attribute("innerText").strip(),
    #                     "Resolved Date": cells[5].get_attribute("innerText").strip()
    #                 }
    #                 all_data.append(entry)
    #
    #         # Switch back to parent window
    #         time.sleep(2)
    #         self.driver.switch_to.window(parent_handle)
    #         print("[INFO]: RETURNED TO PARENT WINDOW")
    #
    #         return True, all_data
    #
    #     except Exception as e:
    #         print(f"[ERROR] Failed to extract activity log data: {e}")
    #         # Attempt to switch back to parent window even on failure
    #         try:
    #             self.driver.switch_to.window(parent_handle)
    #             print("[INFO]: RETURNED TO PARENT WINDOW (after failure)")
    #         except Exception as ex:
    #             print(f"[ERROR] Failed to switch back to parent window: {ex}")
    #         return False, []

#new comment code
    # def extract_activity_log_table_data(self, parent_handle):
    #     try:
    #         # Wait for table to be visible
    #         WebDriverWait(self.driver, 10).until(
    #             EC.visibility_of_element_located((By.XPATH, "//table[@id='bugTable']/tbody/tr[1]/td[1]"))
    #         )
    #
    #         rows = self.driver.find_elements(By.XPATH, "//table[@id='bugTable']/tbody/tr")
    #         all_data = []
    #
    #         for row in rows:
    #             cells = row.find_elements(By.TAG_NAME, "td")
    #             if len(cells) >= 6:
    #                 entry = {
    #                     "Title": cells[0].get_attribute("innerText").strip(),
    #                     "Assignee": cells[1].get_attribute("innerText").strip(),
    #                     "Reporter": cells[2].get_attribute("innerText").strip(),
    #                     "Status": cells[3].get_attribute("innerText").strip(),
    #                     "Assigned Date": cells[4].get_attribute("innerText").strip(),
    #                     "Resolved Date": cells[5].get_attribute("innerText").strip()
    #                 }
    #                 all_data.append(entry)
    #
    #         # ✅ Switch back to parent window
    #         time.sleep(2)
    #         self.driver.switch_to.window(parent_handle)
    #         print("[INFO]: RETURNED TO PARENT WINDOW")
    #
    #         return all_data

    # def extract_full_user_activity_table_data(self):
    #     all_data = []
    #
    #     while True:
    #         try:
    #             # Wait for table rows
    #             WebDriverWait(self.driver, 10).until(
    #                 EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr"))
    #             )
    #             rows = self.driver.find_elements(By.XPATH, "//table/tbody/tr")
    #
    #             for row in rows:
    #                 cells = row.find_elements(By.TAG_NAME, "td")
    #                 if len(cells) >= 6:
    #                     row_data = {
    #                         "Title": cells[0].text.strip(),
    #                         "Assignee": cells[1].text.strip(),
    #                         "Reporter": cells[2].text.strip(),
    #                         "Status": cells[3].text.strip(),
    #                         "Assigned Date": cells[4].text.strip(),
    #                         "Resolved Date": cells[5].text.strip(),
    #                         # You can include "Actions" column if needed:
    #                         # "Actions": cells[6].text.strip() if len(cells) > 6 else ""
    #                     }
    #                     all_data.append(row_data)
    #
    #             # Check for "Next" button
    #             next_button = self.driver.find_element(By.XPATH, "//a[.='Next']")
    #             if "disabled" in next_button.get_attribute("class") or not next_button.is_enabled():
    #                 break
    #             next_button.click()
    #             time.sleep(2)
    #
    #         except Exception as e:
    #             print(f"[INFO] Pagination complete or error occurred: {e}")
    #             break
    #
    #     return all_data






