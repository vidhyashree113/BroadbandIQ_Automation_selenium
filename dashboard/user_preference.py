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
from ..locators.login_locators import LoginPageLocators
from ..pages.common import BasePage
from ..resources.login_page import LoginPage
from selenium.webdriver.support.select import Select
from prettytable import PrettyTable
from datetime import datetime
import time, os


class UserPreference(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def click_user_preference(self):
        try:
            user_link = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LoginPageLocators.USER_LINK)
            )
            user_link.click()
            time.sleep(2)

            preference = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(LoginPageLocators.PREFERENCE)
            )
            preference.click()
            print("[INFO] : CLICKED ON PREFERENCE")
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO CLICK ON PREFERENCE')
            return False

    def click_chevron_icon(self):
        try:
            arrow_click = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LensLocators.ARROW_ICON)
            )
            arrow_click.click()
            print('[INFO] : CLICKED ON CHEVRON ICON')
            time.sleep(2)
            return True
        except Exception as e:
            print('[ERROR] : FAILED TO CLICK ON CHEVRON ICON')
            return False

    def drag_and_drop_lens(self, lens_file_name):
        try:
            # Close popup if it's blocking the lens
            self.close_popup_if_present()

            # Wait for lens element
            lens_path = LensLocators.CHEVRON_LENS_IMAGE_BY_FILENAME(lens_file_name)
            lens_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(lens_path)
            )

            # Ensure lens is visible and not blocked
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(lens_path)
            )

            # Locate drop target
            drop_target = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(LensLocators.DROP_BUTTON)
            )

            # Perform drag and drop
            actions = ActionChains(self.driver)
            actions.click_and_hold(lens_element).pause(1)
            actions.move_to_element(drop_target).pause(1)
            actions.release().perform()

            print(f"[INFO] Lens '{lens_file_name}' dragged and dropped.")
            self.close_popup_if_present()
            return True

        except Exception as e:
            print(f"[ERROR] Drag and drop failed for '{lens_file_name}': {e}")
            self.close_popup_if_present()
            return False

    def is_lens_dropped(self, lens_file_name):
        try:
            lens_path = LensLocators.CHEVRON_LENS_IMAGE_BY_FILENAME(lens_file_name)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(lens_path)
            )
            print(f"[INFO] Lens '{lens_file_name}' was successfully dropped.")
            return True
        except TimeoutException:
            print(f"[ERROR] Lens '{lens_file_name}' not found in drop area.")
            return False



    #old code
    def close_popup_if_present(self):
        """Closes info dialog if lens can't be enabled in user preference mode."""
        try:
            close_btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(LensLocators.DIALOG_CLOSE)
            )
            close_btn.click()
            print("[INFO] Closed popup blocking lens drop.")
            return True
        except TimeoutException:
            return False


    def drag_and_drop_tool(self,tool_name):
        try:
            # Close popup if it's blocking the lens
            self.close_popup_if_present()

            # Wait for lens element
            tool_xpath = LensLocators.RIGHT_SIDE_ICON_TOOL_NAME(tool_name)
            tool_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(tool_xpath)
            )

            # Ensure lens is visible and not blocked
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(tool_xpath)
            )

            # Locate drop target
            drop_target = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(LensLocators.DROP_BUTTON)
            )

            # Perform drag and drop
            actions = ActionChains(self.driver)
            actions.click_and_hold(tool_element).pause(1)
            actions.move_to_element(drop_target).pause(1)
            actions.release().perform()

            print(f"[INFO] Tool '{tool_name}' dragged and dropped.")
            return True

        except Exception as e:
            print(f"[ERROR] Drag and drop failed for '{tool_name}': {e}")
            self.close_popup_if_present()
            return False

    def is_tool_dropped(self, tool_name):
        try:
            tool_xpath = LensLocators.RIGHT_SIDE_ICON_TOOL_NAME(tool_name)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(tool_xpath))
            print(f"[INFO] Tool '{tool_name}' was successfully dropped.")
            return True
        except TimeoutException:
            print(f"[ERROR] Tool '{tool_name}' not found in drop area.")
            return False


    def submit_button(self):
        try:
            time.sleep(2)
            sub_btn = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(LensLocators.PREFERENCE_SUBMIT)
            )
            sub_btn.click()
            print('[INFO] : CLICKED ON SUBMIT BUTTON')
            preference_confirm = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(LensLocators.PREFERENCE_CONFIRM)
            )
            preference_confirm.click()
            print('[INFO] : CLICK ON SUBMIT AFTER CONFIRMING')
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO CLICK ON SUBMIT')
            return False

    def is_lens_visible_in_chevron_panel(self, lens_file_name):
        try:
            time.sleep(5)
            # Ensure chevron is expanded so lenses are visible
            # self.click_chevron_icon()

            lens_path = LensLocators.CHEVRON_LENS_IMAGE_BY_FILENAME(lens_file_name)

            # Wait until the image is in the DOM and visible
            lens_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(lens_path)
            )

            print(f"[INFO] Lens '{lens_file_name}' is displayed in the tool panel.")
            # self.click_chevron_icon()
            return True
            # if lens_element.is_displayed():
            #     print(f"[INFO] Lens '{lens_file_name}' is displayed in the tool panel.")
            #     return True
            # else:
            #     print(f"[ERROR] Lens '{lens_file_name}' found but not visible.")
            #     return False

        except Exception as e:
            print(f"[ERROR] Lens '{lens_file_name}' not found or not visible: {e}")
            return False

    def is_tool_presence(self,tool_name):
        try:
            time.sleep(5)
            # Ensure chevron is expanded so lenses are visible

            tool_xpath = LensLocators.RIGHT_SIDE_ICON_TOOL_NAME(tool_name)
            # Wait until the image is in the DOM and visible
            lens_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(tool_xpath)
            )
            print(f"[INFO] Lens '{tool_name}' is displayed in the tool panel.")
            return True

        except Exception as e:
            print(f"[ERROR] Lens '{tool_name}' not found or not visible: {e}")
            return False


    def logout_and_reset(self):
        try:
            user_link = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LoginPageLocators.USER_LINK)
            )

            user_link.click()
            time.sleep(2)

            logout_button = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable(LoginPageLocators.LOGOUT_BUTTON)
            )
            logout_button.click()
            print('[INFO] : CLICKED on LOGOUT BUTTON')

            logout_confirm = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable(LoginPageLocators.LOGOUT_CONFIRM_BUTTON)
            )
            logout_confirm.click()
            print('[INFO] : CLICKED on LOGOUT CONFIRM BUTTON')

            time.sleep(5)
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO CLICK ON LOGOUT')
            return False


    def reset_preference(self):
        try:
            user_link = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(LoginPageLocators.USER_LINK)
            )
            user_link.click()
            time.sleep(2)

            preference = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(LoginPageLocators.PREFERENCE)
            )
            preference.click()
            print("[INFO] : CLICKED ON PREFERENCE")
            time.sleep(3)

            #clicking on reset preference
            reset_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(LensLocators.PREFERENCE_RESET)
            )
            reset_btn.click()
            print('[INFO] : CLICKED ON RESET BUTTON')
            preference_confirm = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(LensLocators.PREFERENCE_CONFIRM)
            )
            preference_confirm.click()
            print('[INFO] : CLICK ON RESET AFTER CONFIRMING')
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO RESET')
            return False





