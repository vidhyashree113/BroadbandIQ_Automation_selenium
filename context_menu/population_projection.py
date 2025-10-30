# from traceback import print_tb
import pytest
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


class PopulationProjection(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def right_click_population_projection(self):
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
                EC.visibility_of_element_located(Context_Menu_Locators.POPULATION_PROJECTION)
            )
            actions.move_to_element(pole_owner).click().perform()
            time.sleep(2)
            print("[INFO] : CLICKED ON POPULATION_PROJECTION")
            return True

        except Exception as e:
            print(f'[ERROR] : POPULATION_PROJECTION FAILED --> {e}')
            return False


    def select_ssp_dropdown(self):
        try:

            #check for dropdown is present of not
            # Check if dropdown is displayed
            if not WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(Context_Menu_Locators.POPULATION_SSP)
            ):
                print("[WARNING] SSP dropdown is not visible.")
                return False

            # dropdown_check = WebDriverWait(self.)
            #dropdown
            dropdown_element = WebDriverWait(self.driver,20).until(
                EC.presence_of_element_located(Context_Menu_Locators.POPULATION_SSP)
            )

            dropdown = Select(dropdown_element)
            options = dropdown.options

            for i in range(0,len(options)):
                dropdown_text = options[i].text   #capturing dropdown value
                dropdown.select_by_index(i)
                time.sleep(5)

                WebDriverWait(self.driver, 10).until(
                    EC.text_to_be_present_in_element(
                        Context_Menu_Locators.POPULATION_APPLIED_FILTERS, dropdown_text.split(":")[1].strip()
                    )
                )

                #printing Total Population
                population = WebDriverWait(self.driver,20).until(
                    EC.presence_of_element_located(Context_Menu_Locators.POPULATION_VALUE)
                )
                population_value = population.text.strip()

                #SSP filters
                applied_filter = WebDriverWait(self.driver,30).until(
                    EC.presence_of_element_located(Context_Menu_Locators.POPULATION_APPLIED_FILTERS)
                )
                applied_filter_value = applied_filter.text.strip()

                print(f'Selected Dropdown Option : {dropdown_text}\n'
                      f'Total Population : {population_value}\n'
                      f'Applied filter : {applied_filter_value}')

                self.gender_population_data()

                # Capture Race Data
                self.race_population_data()

                # Capture Age Data
                self.click_age_table()

            return True

        except Exception as e:
            print(f'[ERROR] : DROPDOWN WORK FLOW FAILED --> {e}')
            return False

    def gender_population_data(self):
        try:
            gender_tab = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(Context_Menu_Locators.SSP_GENDER)
            )
            gender_tab.click()
            print('[INFO] CLICKED ON GENDER TAB')
            time.sleep(4)
            # waiting for gender table display
            # gender_table_view = WebDriverWait(self.driver, 20).until(
            #     EC.presence_of_element_located(LensLocators.GENDER_TABLE)
            # )
            WebDriverWait(self.driver, 20).until(
                lambda driver: len(driver.find_elements(*Context_Menu_Locators.GENDER_TABLE_ROWS)) >= 2
            )

            # waiting for gender table rows

            gender_table_rows = self.driver.find_elements(*Context_Menu_Locators.GENDER_TABLE_ROWS)

            gender_data = []
            for row in gender_table_rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 2:
                    gender_data.append((cells[0].text.strip(), cells[1].text.strip()))
                # return gender_data

            if gender_data:
                print("[INFO] Gender Population Data:")
                for label, count in gender_data:
                    print(f"{label}: {count}")
                return True
            else:
                print("[WARNING] No gender data found.")
                return False

        except Exception as e:
            print(f"[ERROR] Failed to retrieve race data: {e}")
            return False

    def race_population_data(self):
        try:
            race_tab = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(Context_Menu_Locators.SSP_RACE)
            )
            race_tab.click()
            print('[INFO] CLICKED ON RACE TAB')
            time.sleep(4)
            # waiting for gender table display
            race_table_view = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(Context_Menu_Locators.RACE_TABLE)
            )
            # WebDriverWait(self.driver, 20).until(
            #     lambda driver: len(driver.find_elements(*LensLocators.GENDER_TABLE_ROWS)) >= 2
            # )

            # waiting for gender table rows

            race_table_rows = self.driver.find_elements(*Context_Menu_Locators.RACE_TABLE_ROWS)

            race_data = []
            for row in race_table_rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 2:
                    race_data.append((cells[0].text.strip(), cells[1].text.strip()))
                # return race_data
            if race_data:
                print("[INFO] Gender Population Data:")
                for label, count in race_data:
                    print(f"{label}: {count}")
                return True
            else:
                print("[WARNING]  No Race data found.")
                return False

        except Exception as e:
            print(f"[ERROR] Failed to retrieve race data: {e}")
            return False

    def population_year_slider(self,offset):
        try:
            slider_button = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(Context_Menu_Locators.SSP_YEAR_SLIDER)
            )
            print("[INFO] Year slider is clickable.")

            #performing dragging
            actions = ActionChains(self.driver)
            actions.move_to_element(slider_button).click_and_hold().move_by_offset(offset, 0).release().perform()
            print(f"[INFO] Slider adjusted by offset: {offset}")

            year_label = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Context_Menu_Locators.SSP_YEAR_SLIDER_VALUE)  # <-- Add correct locator here
            )
            selected_year = year_label.text.strip()

            print(f"Year selected after sliding: {selected_year}")
            time.sleep(2)
            close = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(Context_Menu_Locators.POPULATION_MENU_CLOSE)
            )
            close.click()
            print('[INFO] : POPULATION DIALOG BOX CLOSED')
            return True
            # return True  # **Return success**

        except Exception as e:
            print(f"[ERROR] Failed to adjust slider: {e}")
            return False

    def click_age_table(self):
        try:
            # Click on AGE tab
            age_tab = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(Context_Menu_Locators.SSP_AGE)
            )
            age_tab.click()
            print('[INFO] CLICKED ON AGE TAB BUTTON')
            time.sleep(2)

            # Click on AGE Table button
            age_table = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(Context_Menu_Locators.POPULATION_AGE_TABLE_BUTTON)
            )
            age_table.click()
            print('[INFO] CLICKED ON AGE TABLE BUTTON')
            time.sleep(2)

            # Locate search field and enter age
            search = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(Context_Menu_Locators.AGE_TABLE_SEARCH)
            )
            search.clear()
            search.send_keys(AGE_SEARCH)
            print(f"[INFO] Entered Age Group: {AGE_SEARCH}")
            time.sleep(2)

            # Wait for table data to appear
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(Context_Menu_Locators.AGE_TABLE_DATA)
            )

            # Extract table data
            age_table_rows = self.driver.find_elements(*Context_Menu_Locators.AGE_TABLE_ROWS)
            age_present = []

            for row in age_table_rows:
                age_data = row.find_elements(By.TAG_NAME, "td")
                if len(age_data) >= 2 and age_data[0].text.strip() == AGE_SEARCH:
                    age_present.append(age_data[1].text.strip())

            if age_present:
                print(f"[INFO] Population data found for age '{AGE_SEARCH}': {age_present[0]}")
            else:
                print(f"[WARNING] No population data found for age '{AGE_SEARCH}'")

            # ✅ Clear the search box after processing
            search.clear()
            print(f"[INFO] Cleared age input after getting population")

            # Switch back to chart
            age_table.click()
            time.sleep(2)


            #clicking on close button


            return True

        except Exception as e:
            print(f"[ERROR] Failed to get population by age: {e}")
            return False

    # def click_age_table(self):
    #     try:
    #         age_tab = WebDriverWait(self.driver,20).until(
    #             EC.element_to_be_clickable(Context_Menu_Locators.SSP_AGE)
    #         )
    #         age_tab.click()
    #         print('[INFO] CLICKED ON AGE TAB BUTTON')
    #         time.sleep(2)
    #
    #         age_table = WebDriverWait(self.driver,30).until(
    #             EC.element_to_be_clickable(Context_Menu_Locators.POPULATION_AGE_TABLE_BUTTON)
    #         )
    #         age_table.click()
    #         print('[INFO] CLICKED ON AGE TABLE BUTTON')
    #         time.sleep(2)
    #         #searching for age group
    #
    #         search = WebDriverWait(self.driver,30).until(
    #             EC.presence_of_element_located(Context_Menu_Locators.AGE_TABLE_SEARCH)
    #         )
    #         search.send_keys(AGE_SEARCH)   #taking value from config.py file  [10-14]
    #
    #         #Waiting for table data to appear
    #
    #         age_table_data = WebDriverWait(self.driver,20).until(
    #             EC.presence_of_element_located(Context_Menu_Locators.AGE_TABLE_DATA)
    #         )
    #
    #         age_table_rows = self.driver.find_elements(*Context_Menu_Locators.AGE_TABLE_ROWS)
    #         age_present = []
    #         for row in age_table_rows:
    #             age_data = row.find_elements(By.TAG_NAME, "td")
    #             if len(age_data) >= 2 and age_data[0].text.strip() == AGE_SEARCH:
    #                 age_present.append(age_data[1].text.strip())  # Return population count
    #
    #         print(f"Population data found for age {AGE_SEARCH} is {age_present[0]}")
    #
    #         #Switching back to chart
    #         age_table.click()
    #         time.sleep(2)
    #         return True
    #
    #     except Exception as e:
    #         print(f"[ERROR] Failed to get population by age: {e}")
    #         return False


    def population_close(self):
        try:
            close = WebDriverWait(self.driver,20).until(
                EC.element_to_be_clickable(Context_Menu_Locators.POPULATION_MENU_CLOSE)
            )
            close.click()
            print('[INFO] CLICKED ON CLOSE BUTTON')
            return True
        except Exception as e:
            print('[ERROR] FAILED TO POPULATION CLOSE')
            return False







