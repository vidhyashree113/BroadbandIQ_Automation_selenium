import os
import time
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from ..config.config import *
from ..pages.common import BasePage

class FTTH_INSIGHTS(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def open_ftth_insights(self):
        wait = WebDriverWait(self.driver, 20)
        actions = ActionChains(self.driver)

        # Right-click on map and open FTTH Insights
        map_element = wait.until(EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Map']")))
        actions.context_click(map_element).perform()

        ftth_insights = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'FTTH Insights')]")))
        ftth_insights.click()

        time.sleep(5)

        # Task 1: Read Excel data
        excel_df = self._get_expected_ftth_data(FIBER_DATA)

        # Task 2: Fetch UI data
        ui_data = self._get_ui_ftth_data()

        # Task 3: Compare both
        matched, mismatches = self._compare_ftth_data(excel_df, ui_data)

        print("\n✅ Matched Companies:")
        for row in matched:
            print(row)

        print("\n❌ Mismatched or Missing Companies:")
        for row in mismatches:
            print(row)

        print("\n--- Summary ---")
        print(f"✅ Total Matched: {len(matched)}")
        print(f"❌ Total Mismatches or Missing: {len(mismatches)}")

        # Close the popup
        close_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='fiber-close-btn']")))
        close_button.click()

        return True

    def _get_expected_ftth_data(self, excel_path):
        df = pd.read_excel(excel_path)
        companies = [
            "AT&T Inc.",
            "Charter Communications",
            "Uniti Group Inc.",
            "Central Alabama Electric Cooperative"
        ]
        df = df[df["holding_company"].isin(companies)]
        df = df.fillna(0).astype(str)
        return df

    def _get_ui_ftth_data(self):
        wait = WebDriverWait(self.driver, 20)
        table_xpath = "//table[@id='fiber-table']//tbody/tr"
        rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_xpath)))

        ui_data = {}
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if not cells:
                continue

            holding_company = cells[0].text.strip()
            values = [cell.text.strip().replace(",", "") for cell in cells[1:] if cell.get_attribute("class") != "trends_col"]
            ui_data[holding_company] = values

        return ui_data

    def _compare_ftth_data(self, excel_df, ui_data):
        matched = []
        mismatches = []

        for _, row in excel_df.iterrows():
            company = row["holding_company"]
            expected_values = row.drop("holding_company").tolist()
            ui_values = ui_data.get(company)

            if not ui_values:
                mismatches.append((company, "❌ Missing in UI"))
                continue

            row_match = True
            for i, (expected, actual) in enumerate(zip(expected_values, ui_values)):
                if str(expected).strip() != str(actual).strip():
                    mismatches.append((company, f"❌ Mismatch at column {i + 1}", expected, actual))
                    row_match = False

            if row_match:
                matched.append((company, "✅ All values matched"))

        print("\n✅ Matched Companies:")
        for row in matched:
            print(row)

        print("\n❌ Mismatched or Missing Companies:")
        for row in mismatches:
            print(row)

        return matched, mismatches

