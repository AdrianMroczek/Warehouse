from playwright.sync_api import expect

class CatalogPage:
    def __init__(self, page):

        self.page = page

        self.price_filter = page.locator("#priceFilter")
        self.filter_button = page.locator("#applyFilters")
        self.name_filter = page.locator("#nameFilter")
        self.category_filter = page.locator("#categoryFilter")
        self.availability_filter = page.locator("#availabilityFilter")

### Methods for locators and assertions ###
    def set_name_filter(self, name: str):
        self.name_filter.fill(name)

    def select_category(self, category: str):
        self.category_filter.select_option(category)

    def set_max_price(self, price: str):
        self.price_filter.fill(str(price))

    def select_availability(self, availability: str):
        self.availability_filter.select_option(availability)

    def apply_filter(self):
        self.filter_button.click()

    def products_list(self, expected_names: list):
        product_names = self.page.locator("tbody tr td:first-child")
        expect(product_names).to_have_text(expected_names)

### Action methods ###

    def get_order_button_by_name(self, product_name: str):
        return self.page.locator("tr").filter(has_text=product_name).get_by_role("button", name="Zamów")

    def order_product(self, product_name: str, quantity: int):
        row = self.page.locator("tr").filter(has_text=product_name)
        row.locator("input[type='number']").fill(str(quantity))
        self.get_order_button_by_name(product_name).click()


### Check methods ###

    def check_order_button_status(self, product_name: str, expected_status: str):
        button = self.get_order_button_by_name(product_name)
        if expected_status == "enabled":
            expect(button).not_to_be_disabled()
        elif expected_status == "disabled":
            expect(button).to_be_disabled()
        else:
            raise ValueError("Invalid expected status. Use 'enabled' or 'disabled'.")

    def check_availability(self, product_name: str, expected_availability: str):
        row = self.page.locator("tr").filter(has_text=product_name)
        availability_cell = row.locator("td").nth(3).locator("span")
        if expected_availability == "not available":
            expect(availability_cell).to_have_class("badge bg-danger")
        elif expected_availability == "available":
            expect(availability_cell).to_have_class("badge bg-success")
        else:
            raise ValueError("Invalid expected availability. Use 'available' or 'not available'.")

    def check_amount(self, product_name: str, expected_amount: str):
        row = self.page.locator("tr").filter(has_text=product_name)
        amount_cell = row.locator("td").nth(3).locator("span")
        expect(amount_cell).to_contain_text(expected_amount)

    def check_price(self, product_name: str, expected_price: str):
        row = self.page.locator("tr").filter(has_text=product_name)
        price_cell = row.locator("td").nth(2)
        expect(price_cell).to_contain_text(expected_price)