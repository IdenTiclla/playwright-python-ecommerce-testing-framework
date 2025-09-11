from pages.base_page import BasePage
from components.notification import Notification
from components.header_actions import HeaderActions
from components.review_form import ReviewForm
from components.related_products import RelatedProducts
from components.quick_view_modal import QuickViewModal
from components.contact_form import ContactForm
class ProductPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        
        # Components
        self.notification = Notification(page)
        self.header_actions = HeaderActions(page)
        self.review_form = ReviewForm(page)
        self.related_products = RelatedProducts(page)
        self.quick_view_modal = QuickViewModal(page)
        self.contact_form = ContactForm(page)

        # Locators
        self.wishlist_button = page.locator("div#product-product div.content-image.d-none button")
        self.product_name = page.locator("div[class*='content-title'] h1")
        self.product_price = page.locator("div.price h3")
        self.product_availability = page.locator("span[class='badge badge-danger'], span[class='badge badge-success']")
        self.decrease_quantity_button = page.locator("div[class='entry-row row order-3 no-gutters '] button[aria-label='Decrease quantity']")
        self.quantity_input = page.locator("div[class='entry-row row order-3 no-gutters '] input[name='quantity']")
        self.increase_quantity_button = page.locator("div[class='entry-row row order-3 no-gutters '] button[aria-label='Increase quantity']")
        
        self.add_to_cart_button = page.locator("//div[@class='entry-row row order-3 no-gutters ']//button[normalize-space(text()) = 'Add to Cart']")
        
        self.compare_this_product_button = page.locator("div[data-id='216844'] button[title='Compare this Product']")
        self.size_chart_button = page.locator("div[class='entry-row row order-10 order-sm-8 order-md-7 '] a").nth(0)
        self.popup_button = page.locator("div[class='entry-row row order-10 order-sm-8 order-md-7 '] a").nth(1)
        self.ask_question_button = page.locator("div[class='entry-row row order-10 order-sm-8 order-md-7 '] a").nth(2)

        self.tab_list = page.locator("div.d-none.d-md-block ul[role='tablist'] li")
        self.tab_content = page.locator("div.d-none.d-md-block div.tab-content")


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
    
    def add_product_to_wishlist(self):
        """Add the product to the wishlist"""
        self.wishlist_button.click()

    def get_active_tab(self):
        """Get the active tab"""
        return self.tab_list.locator("a.active").text_content().strip()

    def get_inactive_tabs(self):
        """Get the inactive tabs"""
        # apply strip method to each item on the list
        return [item.strip() for item in self.tab_list.locator("a:not(.active)").all_text_contents()]

    def switch_to_tab(self, tab_name: str):
        """Switch to a specific tab"""
        self.tab_list.locator(f"a:has-text('{tab_name}')").click()
        self.page.wait_for_timeout(200)

    def get_tab_content(self, tab_name: str):
        """Get the tab content"""
        if tab_name == "Description":
            return self.tab_content.locator("p.intro").text_content().strip()
        elif tab_name == "Reviews":
            return self.tab_content.locator("div.review").text_content().strip()
        elif tab_name == "Custom":
            return self.tab_content.locator("div.alert").text_content().strip()
        else:
            raise ValueError(f"Invalid tab name: {tab_name}. Use 'Description', 'Reviews', or 'Custom'")

    def is_tab_content_visible(self, tab_name: str):
        """Check if the tab content is visible"""
        if tab_name == "Description":
            return self.tab_content.locator("p.intro").is_visible()
        elif tab_name == "Reviews":
            return self.tab_content.locator("div.review").is_visible()
        elif tab_name == "Custom":
            return self.tab_content.locator("div.alert").is_visible()
        else:
            raise ValueError(f"Invalid tab name: {tab_name}. Use 'Description', 'Reviews', or 'Custom'")

    def click_on_ask_question_button(self):
        """Click on the ask question button"""
        self.ask_question_button.click()
        self.page.wait_for_timeout(200)
