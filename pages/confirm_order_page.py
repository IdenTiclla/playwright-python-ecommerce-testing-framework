from pages.base_page import BasePage
from playwright.sync_api import Page

class ConfirmOrderPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # Locators
        self.page_title = self.page.locator("div.content h1")
        self.products = self.page.locator("table.table-bordered tbody tr")
        self.sub_total = self.page.locator("//table[contains(@class, 'table-bordered')]//td[contains(., 'Sub-Total:')]/following-sibling::td")
        self.flat_shipping_rate = self.page.locator("//table[contains(@class, 'table-bordered')]//td[contains(., 'Flat Shipping Rate:')]/following-sibling::td")
        self.total = self.page.locator("//table[contains(@class, 'table-bordered')]//td[normalize-space(.)='Total:']/following-sibling::td")
        self.confirm_order_button = self.page.locator("button#button-confirm")

    def click_on_confirm_order_button(self):
        """Click on the confirm order button"""
        self.confirm_order_button.click()

    def get_order_information(self):
        products = []
        
        # Wait for the page to be fully loaded
        self.page.wait_for_load_state("networkidle")
        
        # Get all rows from the table using xpath (same approach as sub_total)
        product_rows = self.page.locator("//table[contains(@class, 'table-bordered')]//tr")
        
        # Iterate through all rows and check which ones have 5 cells (product rows)
        for i in range(product_rows.count()):
            row = product_rows.nth(i)
            cells = row.locator("td")
            cells_count = cells.count()
            
            # Only process rows that have 5 columns (product rows)
            if cells_count == 5:
                product_name = cells.nth(0).text_content().strip()
                
                # Skip the header row (contains "Product Name")
                if product_name == "Product Name":
                    continue
                
                product_model = cells.nth(1).text_content().strip()
                product_quantity = cells.nth(2).text_content().strip()
                product_price = cells.nth(3).text_content().strip()
                product_total = cells.nth(4).text_content().strip()
                
                products.append({
                    "name": product_name,
                    "model": product_model,
                    "quantity": product_quantity,
                    "price": product_price,
                    "total": product_total,
                })

        return {
            "products": products,
            "sub_total": round(float(self.sub_total.text_content().strip("$")), 2),
            "flat_shipping_rate": round(float(self.flat_shipping_rate.text_content().strip("$")), 2),
            "total": round(float(self.total.text_content().strip("$")), 2),
        }