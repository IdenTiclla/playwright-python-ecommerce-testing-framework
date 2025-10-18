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
    