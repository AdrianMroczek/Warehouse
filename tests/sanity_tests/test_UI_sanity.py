from playwright.sync_api import expect
from tests.pages.catalog_page import CatalogPage

def test_filter_by_max_price(page):
    catalog = CatalogPage(page)
    page.goto("http://127.0.0.1:8000/")
    expect(page).to_have_title("Warehouse System - Widok Klienta")
    catalog.set_max_price(400)
    catalog.apply_filter()
    catalog.products_list(["Logitech Lift"])

def test_filter_by_category(page):
    catalog = CatalogPage(page)
    page.goto("http://127.0.0.1:8000/")
    expect(page).to_have_title("Warehouse System - Widok Klienta")
    catalog.select_category("Laptopy")
    catalog.apply_filter()
    catalog.products_list(["ASUS ROG Strix G16"])

def test_double_filter(page):
    catalog = CatalogPage(page)
    page.goto("http://127.0.0.1:8000/")
    expect(page).to_have_title("Warehouse System - Widok Klienta")
    catalog.set_name_filter("Lenovo")
    catalog.select_category("Monitory")
    catalog.apply_filter()
    catalog.products_list(["Lenovo Legion 27Q-10"])


