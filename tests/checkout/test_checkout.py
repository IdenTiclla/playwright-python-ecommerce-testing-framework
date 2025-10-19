from tests.base_test import BaseTest
from playwright.sync_api import Page

class TestCheckout(BaseTest):
    
    def test_direct_checkout_with_not_available_product(self):
        # navigate to the home page
        self.home_page.goto()

        # scroll down to the top products section
        self.home_page.top_products.scroll_to_top_products()

        # add third product to the cart
        self.home_page.top_products.add_product_to_cart(index=2)

        # click on the checkout button
        self.home_page.notification.click_on_checkout_button()

        # verify alert message
        alert_messages = self.shopping_cart_page.alert_component.get_alert_messages()
        assert any("Products marked with *** are not available in the desired quantity or not in stock!" in alert_message for alert_message in alert_messages)

        # assert page url
        assert self.page.url == "https://ecommerce-playground.lambdatest.io/index.php?route=checkout/cart"

    def test_direct_checkout_with_available_product_unlogged_user(self):
        # navigate to the home page
        self.home_page.goto()

        # scroll down to the top products section
        self.home_page.top_products.scroll_to_top_products()

        # add third product to the cart
        self.home_page.top_products.add_product_to_cart(index=3)

        # click on the checkout button
        self.home_page.notification.click_on_checkout_button()

        # verify the amount of products in the cart is 1

        cart_count = self.checkout_page.header_actions.get_cart_count()
        assert cart_count == "1"

        # get page url
        get_page_url = self.checkout_page.page.url

        # verify page url
        assert get_page_url == "https://ecommerce-playground.lambdatest.io/index.php?route=checkout/checkout"

        # verify the register radio is selected by default
        assert self.checkout_page.is_register_radio_selected() == True

        # verify the login radio is not selected
        assert self.checkout_page.is_login_radio_selected() == False

        # verify the guest radio is not selected
        assert self.checkout_page.is_guest_radio_selected() == False
