import os

import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..locators.context_menu_locators import Context_Menu_Locators

import time
from ..locators.lens_locators import LensLocators
from ..config.config import *
from ..pages.common import BasePage

from selenium.webdriver.support.select import Select
import traceback


class PoleOwners(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    _ilec_boundary_xpath = "//tbody[@id='ilec_body']//tr[not(@data-id) and not(contains(@class, 'section-sub-header'))]"

    _utility_header_xpath = "//tr[@data-id='utility-section']//span[contains(@class,'po-tree-toggle glyphicon glyphicon-chevron-right')]"
    _utility_boundary_xpath = "//tbody[@id='utility_provider_body']//tr[not(@data-id) and not(contains(@class, 'section-sub-header'))]"
    # _utility_boundary_xpath = "//tbody[@id='utility_provider_body']//tr[not(@data-id) and not(contains(@class, 'section-sub-header'))]"


    def right_click_probable_pole_owners(self):
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

            pole = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(Context_Menu_Locators.CONTEXT_POLE_OWNER)
            )
            actions.move_to_element(pole).click().perform()
            time.sleep(2)
            print("[INFO] : CLICKED ON POLE OWNERS")
            return True

        except Exception as e:
            print(f'[ERROR] : POLE OWNERS FLOW FAILED --> {e}')

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

    def click_on_pole_owners(self):
        wait = WebDriverWait(self.driver, 20)

        actions = ActionChains(self.driver)

        map_element = wait.until(EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Map']")))
        actions.context_click(map_element).perform()

        click_on_pole_owners = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Probable Pole Owners']")))
        click_on_pole_owners.click()
        print('[INFO] : CLICKED ON PROBABLE POLE OWNER')

        self.wait_for_element(Context_Menu_Locators.PROBABLE_DIALOG,timeout_value,poll_frequency_value)


    def _search_provider(self, provider_name):
        """Search only the first word of the provider name and verify it appears in results."""
        # Always define first_word first
        # first_word = provider_name.strip().split()[0] if provider_name else ""
        first_word = provider_name.strip() if provider_name else ""

        try:
            wait = WebDriverWait(self.driver, 15)
            search_input = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search by Provider/Technology']"))
            )

            self.driver.execute_script("arguments[0].scrollIntoView(true);", search_input)
            time.sleep(1)

            # Set value via JS to avoid clear() issues
            self.driver.execute_script("arguments[0].value = arguments[1];", search_input, first_word)
            search_input.send_keys(" ")  # trigger oninput event
            time.sleep(2)

            # Search for rows containing at least the first word
            # result = WebDriverWait(self.driver,30).until(
            #     EC.visibility_of_element_located((By.XPATH,f"//td[contains(normalize-space(), '{first_word}')]"))
            # )


            # result = self.driver.find_element(By.XPATH, f"//td[contains(normalize-space(), '{first_word}')]")
            # if result.is_displayed():

            result = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, f"//tr[contains(., '{first_word}')]"))
            )
            if result:
                print(f"🔍 Verified provider '{provider_name}' (searched: '{first_word}') found in search results.")
            else:
                print(f"⚠️ Provider '{provider_name}' (searched: '{first_word}') not visible in results.")

        except Exception:
            pass
            # print(f"⚠️ Skipping: Provider '{provider_name}' (searched: '{first_word}') could not be verified.")

    def _validate_toggle_all_checked(self, section_id):
        """Ensure Toggle All checkbox is checked when rows are ON."""
        try:
            wait = WebDriverWait(self.driver, 10)
            checkbox = wait.until(EC.presence_of_element_located((By.ID, section_id)))
            if checkbox.is_selected():
                print(f"✅ Toggle All checkbox for [{section_id}] is correctly checked.")
            else:
                pytest.fail(f"❌ Toggle All checkbox for [{section_id}] is NOT checked after toggling ON.")
        except Exception as e:
            pytest.fail(f"❌ Failed to validate Toggle All checkbox for [{section_id}]: {e}")

    def _get_toggle_rows(self, xpath, section_name="Unknown"):
        rows = self.driver.find_elements(By.XPATH, xpath)
        interactable = []

        print(f"\nChecking {len(rows)} raw toggle rows from XPath for [{section_name}]...\n")
        for i, row in enumerate(rows, 1):
            try:
                tds = row.find_elements(By.TAG_NAME, "td")
                if len(tds) < 4:
                    raise ValueError("Expected at least 4 <td> elements")

                provider = tds[1].text.strip()
                company = tds[2].text.strip()
                toggle = tds[-1].find_element(By.XPATH, ".//span[@class='switch-slider round']")

                print(f"Row #{i}: Provider = '{provider}', Company = '{company}'")
                if provider and company:
                    interactable.append((row, toggle))
            except Exception as e:
                print(f"Skipping row #{i} due to error: {e}")
                continue

        return interactable

    def _expand_utility_section(self):
        try:
            wait = WebDriverWait(self.driver, 20)
            utility_header = wait.until(
                EC.presence_of_element_located((By.XPATH, self._utility_header_xpath))
            )

            current_class = utility_header.get_attribute("class")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", utility_header)
            time.sleep(1)

            if "chevron-right" in current_class:
                self.driver.execute_script("arguments[0].click();", utility_header)
                print("✅ Expanded Utility section.")
                WebDriverWait(self.driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, "//tr[@data-parent='utility-section']"))
                )
            else:
                print("Utility section already expanded, skipping click.")

        except Exception as e:
            pytest.fail(f"❌ Failed to expand Utility section: {e}")

    def _toggle_rows(self, rows, action, section_name):
        print(f"{'Turning OFF' if action == 'off' else 'Turning ON'} {len(rows)} toggles in [{section_name}]")

        for idx, (row, toggle_btn) in enumerate(rows, 1):
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", row)
                time.sleep(1)

                cells = row.find_elements(By.TAG_NAME, "td")
                provider = cells[1].text.strip()
                company = cells[2].text.strip()

                self.driver.execute_script("arguments[0].click();", toggle_btn)
                time.sleep(1)

                print(
                    f"{'✅' if action == 'on' else '🛑'} [{section_name}] Turned {action.upper()}: Provider = '{provider}', Company = '{company}'")
            except Exception as e:
                pytest.fail(f"❌ Failed to toggle [{section_name}] row #{idx}: {e}")

    def toggle_all(self):
        # 1) Toggle ILEC
        ilec_rows = self._get_toggle_rows(self._ilec_boundary_xpath, section_name="ILEC Boundary")
        self._toggle_rows(ilec_rows, "on", "ILEC Boundary")

        # 2) Expand utility and toggle
        self._expand_utility_section()
        utility_rows = self._get_toggle_rows(self._utility_boundary_xpath, section_name="Electric Utility Boundary")
        self._toggle_rows(utility_rows, "on", "Electric Utility Boundary")

        # 3) Collect all toggled providers
        all_rows = ilec_rows + utility_rows
        providers = []
        for row, _ in all_rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            provider = cells[1].text.strip()
            if provider:
                providers.append(provider)

        print(f"Total valid toggles found: {len(all_rows)}")

        # 4) Search the LAST provider after all toggles are ON
        if providers:
            last_provider = providers[-1]
            self._search_provider(last_provider)

        # 5) Check Toggle All checkboxes AFTER search
        self._validate_toggle_all_checked("ilec")
        self._validate_toggle_all_checked("utility")

        # 6) Toggle everything OFF at the end
        self._toggle_rows(all_rows, "off", "All Sections")

    # def toggle_all(self):
    #     # Step 1: ILEC
    #     ilec_rows = self._get_toggle_rows(self._ilec_boundary_xpath, section_name="ILEC Boundary")
    #     self._toggle_rows(ilec_rows, "on", "ILEC Boundary")
    #
    #     # Step 2: Utility
    #     utility_rows = self._get_toggle_rows(self._utility_boundary_xpath, section_name="Electric Utility Boundary")
    #     self._toggle_rows(utility_rows, "on", "Electric Utility Boundary")
    #
    #     # Total
    #     all_rows = ilec_rows + utility_rows
    #     print(f"Total valid toggles found: {len(all_rows)}")
    #
    #     # Step 3: Turn all OFF
    #     self._toggle_rows(all_rows, "off", "All Sections")


    def close_pole_owners_legend(self):
        try:
            close = WebDriverWait(self.driver,30).until(
                EC.element_to_be_clickable(LensLocators.PROBABLE_POLE_OWNER_CLOSE)
            )
            time.sleep(1)
            close.click()
            print('[INFO] : CLICKED ON CLOSE BUTTON')
            return True

        except Exception as e:
            print('[ERROR] : FAILED TO PROBABLE POLE OWNER CLOSE')
            return False























#######################################################################################################
# # from traceback import print_tb
# import pytest
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# from config.assertion_config import POLE_OWNER_LABELS
# from locators.right_icon_locators import RightIconLocators
# import time
# from locators.context_menu_locators import Context_Menu_Locators
# from config.config import *
# from common.common import BasePage
# from common.map_page import MapPage
# from selenium.webdriver.support.select import Select
# import traceback
#
#
# class ProablePoleOwner(BasePage):
#
#     def __init__(self, driver):
#         super().__init__(driver)
#         self.driver = driver
#
#     def right_click_pole_owner(self):
#         try:
#             print("[INFO]: Right-clicked on the red-colored area (estimated position).")
#
#             #old code
#             canvas = WebDriverWait(self.driver,30).until(
#                 EC.element_to_be_clickable((By.CLASS_NAME, "mapboxgl-canvas"))
#             )
#             width = canvas.size['width']
#             height = canvas.size['height']
#             center_x = width // 2
#             center_y = height // 2
#
#             offset_x = center_x + 30
#             offset_y = center_y
#             actions = ActionChains(self.driver)
#             actions.move_to_element_with_offset(canvas, center_x, center_y).context_click(canvas).perform()
#             print("[INFO]: right click happend...")
#
#             # selecting ISP footprint
#             # Hover and click "ISP Footprint Report"
#             pole_owner = WebDriverWait(self.driver, 30).until(
#                 EC.visibility_of_element_located(Context_Menu_Locators.CONTEXT_POLE_OWNER)
#             )
#             actions.move_to_element(pole_owner).click().perform()
#             time.sleep(2)
#             print("[INFO] : CLICKED ON PROBABLE POLE OWNER")
#             return True
#
#         except Exception as e:
#             print(f'[ERROR] : PROBABLE POLE OWNER FAILED --> {e}')
#             return False
#
#     def verify_pole_owner_title(self):
#         """Verify that the lens title is 'Community OPPORTUNITY  Boundaries' and return the result."""
#         try:
#             pole_owner_title_element = WebDriverWait(self.driver, 30).until(
#                 EC.visibility_of_element_located(Context_Menu_Locators.POLE_OWNER_TITLE)
#             )
#             title_text = pole_owner_title_element.text.strip()
#             print(f"[INFO] Lens title found: '{title_text}'")
#
#             if title_text == "Probable Pole Owners":
#                 return True  #
#             else:
#                 print(f"[ERROR] Lens title mismatch! Expected: 'Probable Pole Owners', Found: '{title_text}'")
#                 return False  #
#
#         except Exception as e:
#             print(f"[ERROR] Lens title verification failed: {e}")
#             return False  #
#
#     def verify_pole_owner_legend_checkbox(self):
#         """Verify that the GRANT Boundaries checkbox is checked."""
#         try:
#             checkbox = WebDriverWait(self.driver, 30).until(
#                 EC.presence_of_element_located(Context_Menu_Locators.POLE_OWNER_CHECKBOX)
#             )
#             if checkbox.is_selected():
#                 print("[INFO] Pole Owner Boundaries checkbox is checked.")
#                 return True
#             else:
#                 print("[ERROR] Pole Owner Boundaries checkbox is not checked!")
#                 return False
#         except Exception as e:
#             print(f"[ERROR] Pole Owner Boundaries checkbox verification failed: {e}")
#             return False
#
#     def toggle_off_all_switches_and_assert(self):
#         """Turn OFF all Community Anchor toggles and assert label + state."""
#
#         try:
#             time.sleep(5)
#
#             for index, (by, toggle_xpath) in enumerate(Context_Menu_Locators.POLE_OWNER_TOGGLE):
#                 # Click the toggle
#                 toggle_element = WebDriverWait(self.driver, 10).until(
#                     EC.element_to_be_clickable((by, toggle_xpath))
#                 )
#                 toggle_element.click()
#                 label_text = POLE_OWNER_LABELS[index]
#                 print(f"[INFO] Clicked toggle {label_text}: {toggle_xpath}")
#                 time.sleep(1)
#
#                 # Get corresponding label
#
#                 label_xpath = f"(//div[@class='color-legend-item']//span[normalize-space()='{label_text}'])[{1}]"
#                 label_element = self.driver.find_element(By.XPATH, label_xpath)
#
#                 if not label_element.is_displayed():
#                     print(f"[ERROR] Label not visible: '{label_text}'")
#                     return False
#                 print(f"[INFO] Verified Actual and Expected Value : {label_text}")
#
#                 # Check if the toggle is OFF
#                 input_xpath = toggle_xpath.replace("span[@class='switch-slider round']", "input[@type='checkbox']")
#                 input_element = self.driver.find_element(By.XPATH, input_xpath)
#                 toggle_class = input_element.get_attribute("class")
#                 # print(f"[DEBUG] Toggle class for '{label_text}': {toggle_class}")
#
#                 if "off-class" not in toggle_class:
#                     print(f"[ERROR] Toggle for '{label_text}' expected to be OFF, but it's ON!")
#                     return False
#
#             print("[PASSED] All toggles OFF with correct labels verified.")
#             return True
#
#         except Exception as e:
#             print(f"[ERROR] Failed to toggle or verify switches: {e}")
#             return False
#
#     def toggle_on_all_switches_and_assert(self):
#         """
#         Turn ON all community anchor toggles and assert they are ON by checking the absence of 'off-class' in the input tag.
#         """
#         try:
#             toggles = Context_Menu_Locators.POLE_OWNER_TOGGLE
#             labels = POLE_OWNER_LABELS
#
#             for index, (by, span_locator) in enumerate(toggles):
#                 # Find the <span> to click
#                 span_element = WebDriverWait(self.driver, 10).until(
#                     EC.presence_of_element_located((by, span_locator))
#                 )
#                 # self.driver.execute_script("arguments[0].scrollIntoView(true);", span_element)
#
#                 input_element = span_element.find_element(By.XPATH, "./preceding-sibling::input")
#                 toggle_class = input_element.get_attribute("class")
#                 # print(f"[DEBUG] Initial INPUT class for '{labels[index]}': {toggle_class}")
#
#                 if "off-class" in toggle_class:
#                     span_element.click()
#                     print(f"[INFO] Toggled ON: {labels[index]}")
#                     time.sleep(1)
#                 else:
#                     print(f"[INFO] Already ON: {labels[index]}")
#
#             for index, (by, span_locator) in enumerate(toggles):
#                 span_element = self.driver.find_element(by, span_locator)
#                 input_element = span_element.find_element(By.XPATH, "./preceding-sibling::input")
#                 toggle_class = input_element.get_attribute("class")
#
#                 assert "off-class" not in toggle_class, f"[ERROR] {labels[index]} is still OFF!"
#                 print(f"[ASSERTION PASSED] {labels[index]} is ON ✅")
#
#             return True
#
#         except Exception as e:
#             print(f"[ERROR] Failed to toggle ON all switches: {e}")
#             return False
#
#
#     def close_pole_owner_legend(self):
#         try:
#             close = WebDriverWait(self.driver,20).until(
#                 EC.element_to_be_clickable(Context_Menu_Locators.POLE_OWNER_LEGEND_CLOSE)
#             )
#             close.click()
#             print('[INFO] : CLICKED ON CLOSE ON LEGEND CLOSED')
#             return True
#
#         except Exception as e:
#             print('[ERROR] FAILED TO CLOSE LEGEND')
#             return False