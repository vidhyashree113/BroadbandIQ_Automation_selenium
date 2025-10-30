import random
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# import config.config
from ..config.config import *
from ..config.assertion_config import *
from ..locators.lens_locators import LensLocators
from ..locators.login_locators import LoginPageLocators
from ..locators.right_icon_locators import RightIconLocators
from ..pages.map_page import MapPage
from ..pages.common import BasePage
from datetime import datetime
from selenium.webdriver.support.select import Select
import time,os
from ..config.config import *
import time

class DashboardTask(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.served = None

    def activitylog(self):
        try:
            time.sleep(5)
            parent_handle = self.driver.current_window_handle

            # Step 1: Click on user link
            user_link = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LoginPageLocators.USER_LINK)
            )
            user_link.click()
            time.sleep(4)

            # Step 2: Click on dashboard link
            dashboard_tracker = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LoginPageLocators.DASHBOARD)
            )
            dashboard_tracker.click()
            time.sleep(3)
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
                        time.sleep(3)

                        # Step 5: Select VCTI from org dropdown
                        dropdown_element = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(RightIconLocators.ACTIVITY_LOG_DD)
                        )
                        Select(dropdown_element).select_by_visible_text("VCTI")
                        print('[INFO]: SELECTED VCTI ORGANIZATION')
                        time.sleep(2)

                        # Step 6: Select USER from All Users dropdown
                        dropdown_element1 = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(RightIconLocators.ALL_USERS_DD)
                        )
                        Select(dropdown_element1).select_by_value(USERNAME)
                        print(f'[INFO]: SELECTED USER --> {USERNAME}')
                        time.sleep(2)

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
                        username_footer_input.send_keys(USERNAME)
                        print('[INFO]: ENTERED USERNAME IN FOOTER')

                        # Step 9: Enter Activity
                        activity_footer_input = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable(RightIconLocators.FOOTER_ACTIVITY)
                        )
                        activity_footer_input.clear()
                        activity_footer_input.send_keys("Bug list")
                        print('[INFO]: ENTERED ACTIVITY IN FOOTER')
                        time.sleep(15)


                    #
                    except Exception as e1:
                        print(f"[WARNING] Could not interact with tab {handle}: {e1}")

                    finally:
                        print(f'[INFO] CLOSING CHILD WINDOW : {handle}')
                        self.driver.close()
                        # return None

            # Step 10: Return to Parent Window
            time.sleep(2)
            self.driver.switch_to.window(parent_handle)
            print("[INFO]: RETURNED TO PARENT WINDOW")

            return True

        except Exception as e:
            print(f"[ERROR] Failed in activitylog: {e}")
            return False





