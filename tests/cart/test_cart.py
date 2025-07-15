import time
import pytest
import re
from playwright.sync_api import expect
from tests.base_test import BaseTest
from utils.data_generator import generate_random_email, generate_random_first_name, generate_random_last_name, generate_random_phone_number, generate_random_password

@pytest.mark.cart
class TestCart(BaseTest):

    def test_empty_cart_with_new_user(self):
        """
        Verifica que el carrito de compras está vacío para un usuario recién registrado.
        """
        # Flujo de la prueba
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_my_account_option("Register")

        generated_password = generate_random_password()

        # Usamos un email único para cada ejecución de la prueba
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

        self.success_page.wait_for_page_load()
        assert self.home_page.header_actions.get_cart_count() == "0"
        self.home_page.header_actions.click_on_cart_button()
        assert self.home_page.cart_panel.is_visible() == True

        # Usamos los métodos de la clase componente para las aserciones
        message = self.home_page.cart_panel.get_message()
        sub_total = self.home_page.cart_panel.get_sub_total()
        total = self.home_page.cart_panel.get_total()
        
        assert message == "Your shopping cart is empty!"
        assert sub_total == "$0.00"
        assert total == "$0.00"

    def test_adding_product_to_cart_with_new_user(self):
        """
        Verifica que se puede añadir un producto al carrito después de registrar un nuevo usuario.
        """
        # Registering an user
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_my_account_option("Register")
        
        generated_password = generate_random_password()
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

        # Adding a product to the cart
        self.success_page.wait_for_page_load()
        self.home_page.goto()
        self.home_page.top_products.add_product_to_cart(index=0)
        
        # Verifying the notification - USANDO expect() de Playwright
        expect(self.home_page.notification.container).to_be_visible()
        
        expected_message = "Success: You have added iMac to your shopping cart!"
        expect(self.home_page.notification.message).to_have_text(expected_message)
        
        expect(self.home_page.notification.view_cart_button).to_be_visible()
        expect(self.home_page.notification.checkout_button).to_be_visible()

        self.home_page.notification.close()
        expect(self.home_page.notification.container).to_be_hidden()
        
        assert self.home_page.header_actions.get_cart_count() == "1"
        self.home_page.header_actions.click_on_cart_button()
        expect(self.home_page.cart_panel.panel).to_be_visible()
        
        # Después de agregar un producto, el carrito NO debería estar vacío
        # Verificamos que los totales no sean $0.00
        assert self.home_page.cart_panel.get_sub_total() != "$0.00"
        assert self.home_page.cart_panel.get_total() != "$0.00"

