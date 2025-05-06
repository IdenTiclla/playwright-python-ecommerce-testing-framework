import time
from pages.home_page import HomePage
from pages.register_page import RegisterPage
from playwright.sync_api import expect
import pytest

class TestCart:
    def test_empty_cart_with_new_user(self, page):
        home = HomePage(page)
        register_page = RegisterPage(page)
        home.goto()
        home.navbar_horizontal.click_my_account_option("Register")

        register_page.register(
            firstname="Brayan",
            lastname="Mendoza",
            email="test.user" + str(int(time.time())) + "@example.com",
            telephone="+1234567890",
            password="Test@123",
            subscribe_newsletter=True
        )
        # assert cart panel is not visible 
        assert not home.cart_panel.is_visible(), "Cart panel should not be visible" 
        home.click_on_my_cart_button()
        page.wait_for_load_state("domcontentloaded")
        assert home.cart_panel.is_visible(), "Cart panel should be visible"

        # Opción 1: Usar expect (Playwright)
        expect(home.page.locator(home.cart_panel.sub_total)).to_have_text("$0.00")
        expect(home.page.locator(home.cart_panel.total)).to_have_text("$0.00")
        expect(home.page.locator(home.cart_panel.message)).to_have_text("Your shopping cart is empty!")

        # Opción 2: Usar assert con inner_text()
        assert home.page.locator(home.cart_panel.sub_total).inner_text() == "$0.00", "Sub total should be $0.00"
        assert home.page.locator(home.cart_panel.total).inner_text() == "$0.00", "Total should be $0.00"
        assert home.page.locator(home.cart_panel.message).inner_text() == "Your shopping cart is empty!", "Cart message should indicate empty cart"

        # Opción 3: Usar text_content() (puede devolver None si no existe el elemento)
        assert home.page.locator(home.cart_panel.sub_total).text_content() == "$0.00"
        assert home.page.locator(home.cart_panel.total).text_content() == "$0.00"
        assert home.page.locator(home.cart_panel.message).text_content() == "Your shopping cart is empty!"

        # Opción 4: Usar métodos de la clase CartPanel
        
        home.cart_panel.check_sub_total("$0.00")
        home.cart_panel.check_total("$0.00")