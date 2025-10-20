from tests.base_test import BaseTest
import time
from utils.data_generator import generate_random_email, generate_random_first_name, generate_random_last_name, generate_random_phone_number, generate_random_password

class TestCheckout(BaseTest):
    
    def test_direct_checkout_with_not_available_product_unlogged_user(self):
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

        # verify that account radio options are displayed
        assert self.checkout_page.account_radio_options_are_displayed()

        # verify the register radio is selected by default
        assert self.checkout_page.is_register_radio_selected()

        # verify the login radio is not selected
        assert not self.checkout_page.is_login_radio_selected()

        # verify the guest radio is not selected
        assert not self.checkout_page.is_guest_radio_selected()

    def test_direct_checkout_with_available_product_logged_user(self):
        # navigate to the home page
        self.home_page.goto()

        # click on the login option on navbar
        self.home_page.navbar_horizontal.click_my_account_option("Register")

        # generate random password
        generated_password = generate_random_password()

        # register a new user with random data
        self.register_page.register(
            firstname=generate_random_first_name(),
            lastname=generate_random_last_name(),
            email=generate_random_email(),
            telephone=generate_random_phone_number(),
            password=generated_password,
            password_confirm=generated_password,
            subscribe_newsletter=True,
            accept_terms=True
        )

        # go to home page

        self.home_page.goto()

        # scroll down to the top products section
        self.home_page.top_products.scroll_to_top_products()

        # add third product to the cart
        self.home_page.top_products.add_product_to_cart(index=3)

        # click on the checkout button
        self.home_page.notification.click_on_checkout_button()
        
        # verify that account radio options aren't displayed
        assert not self.checkout_page.account_radio_options_are_displayed()
