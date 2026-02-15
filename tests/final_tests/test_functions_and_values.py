from playwright.sync_api import expect
from tests.pages.catalog_page import CatalogPage

def test_filtering(page):
    catalog = CatalogPage(page)
    page.goto("http://127.0.0.1:8000/")
    expect(page).to_have_title("Warehouse System - Widok Klienta")
    catalog.select_category("Laptopy")
    catalog.apply_filter()
    catalog.products_list(["HP 15-FC0001NW", "ASUS TUF Gaming A16 FA608UH-R7165W 16", "DELL Inspiron 3530-8026 15.6"])
    catalog.select_availability("W magazynie")
    catalog.apply_filter()
    catalog.products_list(["HP 15-FC0001NW", "ASUS TUF Gaming A16 FA608UH-R7165W 16"])
    catalog.set_max_price(3000)
    catalog.apply_filter()
    catalog.products_list(["HP 15-FC0001NW"])
    catalog.select_availability("Brak w magazynie")
    catalog.apply_filter()
    catalog.products_list(["DELL Inspiron 3530-8026 15.6"])

def test_checking_values(page):
    catalog = CatalogPage(page)
    page.goto("http://127.0.0.1:8000/")
    expect(page).to_have_title("Warehouse System - Widok Klienta")
    catalog.set_name_filter("Corsair")
    catalog.apply_filter()
    catalog.check_order_button_status("Corsair Katar Pro", "enabled")
    catalog.check_order_button_status("Corsair Scimitar Elite", "disabled")
    catalog.check_availability("Corsair Katar Pro", "available")
    catalog.check_availability("Corsair Scimitar Elite", "not available")
    catalog.check_price("Corsair Katar Pro", "85.40")

def test_ordering_product(page):
    catalog = CatalogPage(page)
    page.goto("http://127.0.0.1:8000/")
    expect(page).to_have_title("Warehouse System - Widok Klienta")
    catalog.select_category("Laptopy")
    catalog.apply_filter()
    catalog.check_amount("HP 15-FC0001NW", "11")
    page.on("dialog", lambda dialog: dialog.accept())
    catalog.order_product("HP 15-FC0001NW", 1)
    catalog.check_amount("HP 15-FC0001NW", "10")
    catalog.order_product("HP 15-FC0001NW", 3)
    catalog.check_amount("HP 15-FC0001NW", "7")
    catalog.check_amount("ASUS TUF Gaming A16 FA608UH-R7165W 16", "6")
    catalog.order_product("ASUS TUF Gaming A16 FA608UH-R7165W 16", 6)
    catalog.check_availability("ASUS TUF Gaming A16 FA608UH-R7165W 16", "not available")
    catalog.check_order_button_status("ASUS TUF Gaming A16 FA608UH-R7165W 16", "disabled")


