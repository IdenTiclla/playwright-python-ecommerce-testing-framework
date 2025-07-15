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
        self.home_page.click_on_my_cart_button()
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
        # --- Parte 1: Registro de Usuario ---
        self.home_page.goto()  # goto() ya espera que la página cargue
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
        
        # Solo necesitamos timeout extendido para URL porque puede tardar más que 5s
        expect(self.page).to_have_url(re.compile(".*account/success"), timeout=10000)
        
        # --- Parte 2: Añadir producto al carrito ---
        self.home_page.goto()
        expect(self.page).to_have_title(re.compile("Your Store"))

        self.home_page.top_products.scroll_to_top_products()
        # scroll ya posiciona, expect() espera automáticamente
        expect(self.page.locator(self.home_page.top_products.section)).to_be_visible()
        
        # add_product_to_cart ya maneja las esperas internas
        self.home_page.top_products.add_product_to_cart(index=0)
        
        # expect() con auto-wait es suficiente para notificaciones
        notification_selector = self.page.locator(self.home_page.notification.container)
        expect(notification_selector).to_be_visible()
        
        # Verificar el mensaje usando expect() que es más robusto que text_content()
        expected_message = "Success: You have added iMac to your shopping cart!"
        notification_message = self.page.locator(self.home_page.notification.message)
        expect(notification_message).to_have_text(expected_message)
        
        # expect() ya espera automáticamente - no necesitamos timeout
        expect(self.page.locator(self.home_page.notification.view_cart_button)).to_be_visible()
        expect(self.page.locator(self.home_page.notification.checkout_button)).to_be_visible()

        # close() ya maneja el click internamente
        self.home_page.notification.close()
        expect(notification_selector).not_to_be_visible()
        
        # --- Parte 3: Verificar el contenido del carrito ---
        self.home_page.click_on_my_cart_button()
        expect(self.home_page.cart_panel.panel).to_be_visible()
        
        # expect() con auto-wait
        expect(self.home_page.cart_panel.message).not_to_be_visible()
        
        # expect() espera automáticamente hasta que el texto no sea $0.00
        expect(self.home_page.cart_panel.sub_total).not_to_have_text("$0.00")
        expect(self.home_page.cart_panel.total).not_to_have_text("$0.00")

