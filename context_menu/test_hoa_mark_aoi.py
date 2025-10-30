import pytest
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from config.config import *
from pages.hoa_mark_aoi import HOAExport
from pages.hoa_lens import HOALens
from pages.map_page import MapPage


@pytest.fixture(scope="function")
def setup(driver, request):
    """Reinitialize map page for each test."""
    map_page = MapPage(driver)
    hoa1 = HOALens(driver)
    hoa = HOAExport(driver)
    time.sleep(30)
    test_name = request.node.name

    yield hoa
    time.sleep(10)

    if "test_right_click_hoa_export_excel" in request.node.name:
        map_page.reset()


@pytest.mark.order(1)
def test_search_county_double_click(setup,driver):
    try:
        map_page = MapPage(driver)
        hoa1 = HOALens(driver)
        hoaboundary = HOAExport(driver)
        time.sleep(20)
        map_page.search_county(COUNTY_NAME)
        assert map_page.is_county_selected(COUNTY_NAME), f"[ERROR] County '{COUNTY_NAME}' not found after search."
        time.sleep(10)
        map_page.double_click_the_county(), f'[ERROR] Map did not double click on {COUNTY_NAME}'
        time.sleep(10)
        map_page.click_icon()
        time.sleep(4)
        map_page.search_lens('Hoa')
        hoa1.click_hoa_lens(),'[ERROR] failed to click on HOA lens'


    except AssertionError as e:
        setup.take_screenshot("test_search_county_double_click_failed")
        raise e


@pytest.mark.order(2)
def test_right_click_mark_AOI(setup,driver):
    try:
        hoaboundary = HOAExport(driver)
        hoa1 = HOALens(driver)
        hoa1.click_hoa_lens(), '[ERROR] failed to click on HOA lens'
        time.sleep(5)

        assert setup.right_click_mark_AOI(),"[ERROR] select MARK AOI failed"

    except AssertionError as e:
        setup.take_screenshot("test_right_click_mark_AOI_failed")
        raise e


@pytest.mark.order(3)
def test_right_click_hoa_export_pdf(setup):
    try:
        assert setup.right_click_hoa_export_pdf(), "[ERROR] Export PDF failed"

    except AssertionError as e:
        setup.take_screenshot("test_right_click_hoa_export_pdf_failed")
        raise e

@pytest.mark.order(3)
def test_right_click_hoa_export_excel(setup):
    try:
        assert setup.right_click_hoa_export_excel(), "[ERROR] Export Excel failed"

    except AssertionError as e:
        setup.take_screenshot("test_right_click_hoa_export_excel_failed")
        raise e