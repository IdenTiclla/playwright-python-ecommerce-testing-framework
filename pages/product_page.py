from pages.base_page import BasePage
from components.notification import Notification
from components.header_actions import HeaderActions
class ProductPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.notification = Notification(page)
        self.header_actions = HeaderActions(page)

        self.wishlist_button = page.locator("btn btn-wishlist wishlist-28").first
        self.product_name = page.locator("div[class*='content-title'] h1")
        self.product_price = page.locator("div.price h3")
        self.product_availability = page.locator("span[class='badge badge-danger'], span[class='badge badge-success']")
        self.decrease_quantity_button = page.locator("div[class='entry-row row order-3 no-gutters '] button[aria-label='Decrease quantity']")
        self.quantity_input = page.locator("div[class='entry-row row order-3 no-gutters '] input[name='quantity']")
        self.increase_quantity_button = page.locator("div[class='entry-row row order-3 no-gutters '] button[aria-label='Increase quantity']")
        
        self.add_to_cart_button = page.locator("//div[@class='entry-row row order-3 no-gutters ']//button[normalize-space(text()) = 'Add to Cart']")
        
        self.compare_this_product_button = page.locator("div[data-id='216844'] button[title='Compare this Product']")
        self.size_chart_button = page.locator("div[class='entry-row row order-10 order-sm-8 order-md-7 '] a").nth(1)
        self.popup_button = page.locator("div[class='entry-row row order-10 order-sm-8 order-md-7 '] a").nth(2)
        self.ask_question_button = page.locator("div[class='entry-row row order-10 order-sm-8 order-md-7 '] a").nth(3)


    def get_product_name(self):
        """Get the product name"""
        return self.product_name.text_content()

    def get_product_availability(self):
        return self.product_availability.text_content()
    
    def get_product_price(self):
        """Get the product price"""
        return self.product_price.text_content()
    
    def get_product_quantity(self):
        """Get the product quantity"""
        return int(self.quantity_input.input_value())
    
    def increase_product_quantity(self):
        """Increase the product quantity"""
        self.increase_quantity_button.click()

    def decrease_product_quantity(self):
        """Decrease the product quantity"""
        self.decrease_quantity_button.click()

    def fill_product_quantity(self, quantity):
        """Fill the product quantity"""
        self.quantity_input.clear()
        self.quantity_input.fill(str(quantity))

    def add_product_to_cart(self, quantity=1):
        """Add the product to the cart"""
        self.fill_product_quantity(quantity)
        self.add_to_cart_button.click()
