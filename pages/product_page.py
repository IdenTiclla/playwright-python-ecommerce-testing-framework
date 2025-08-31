from pages.base_page import BasePage

class ProductPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

        self.wishlist_button = page.locator("btn btn-wishlist wishlist-28").first
        self.product_name = page.locator("div[class*='content-title'] h1")
        self.product_price = page.locator("div.price h3")
        self.product_availability = page.locator("span[class='badge badge-danger'], span[class='badge badge-success']")
        self.decrease_quantity_button = page.locator("div[class='entry-row row order-3 no-gutters '] button[aria-label='Decrease quantity']")
        self.quantity_input = page.locator("div[class='entry-row row order-3 no-gutters '] input[name='quantity']")
        self.increase_quantity_button = page.locator("div[class='entry-row row order-3 no-gutters '] button[aria-label='Increase quantity']")
        self.compare_this_product_button = page.locator("div[data-id='216844'] button[title='Compare this Product']")
        self.size_chart_button = page.locator("div[class='entry-row row order-10 order-sm-8 order-md-7 '] a").nth(1)
        self.popup_button = page.locator("div[class='entry-row row order-10 order-sm-8 order-md-7 '] a").nth(2)
        self.ask_question_button = page.locator("div[class='entry-row row order-10 order-sm-8 order-md-7 '] a").nth(3)


    def get_product_availability(self):
        return self.product_availability.text_content()
    
    def get_product_quantity(self):
        """Get the product quantity"""
        return int(self.quantity_input.input_value())
