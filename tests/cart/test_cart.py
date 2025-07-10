import time
import pytest
import re
from playwright.sync_api import expect
from tests.base_test import BaseTest

@pytest.mark.cart
class TestCart(BaseTest):

    def test_empty_cart_with_new_user(self):
        """
        Verifica que el carrito de compras está vacío para un usuario recién registrado.
        """
        # Flujo de la prueba
        self.home_page.goto()
        self.home_page.navbar_horizontal.click_my_account_option("Register")

        # Usamos un email único para cada ejecución de la prueba
        unique_email = f"test.user.{int(time.time())}@example.com"
        self.register_page.register(
            firstname="Brayan",
            lastname="Mendoza",
            email=unique_email,
            telephone="+1234567890",
            password="Test@123",
            password_confirm="Test@123",
            subscribe_newsletter=True
        )

        # expect() ya tiene auto-wait de 5 segundos - no necesitamos timeout explícito
        expect(self.page.locator(self.home_page.cart_panel.panel)).not_to_be_visible()
        self.home_page.click_on_my_cart_button()  # click() ya espera automáticamente
        expect(self.page.locator(self.home_page.cart_panel.panel)).to_be_visible()

        # Usamos los métodos de la clase componente para las aserciones
        assert self.home_page.cart_panel.check_message("Your shopping cart is empty!")
        assert self.home_page.cart_panel.check_sub_total("$0.00")
        assert self.home_page.cart_panel.check_total("$0.00")

    def test_adding_product_to_cart_with_new_user(self):
        """
        Verifica que se puede añadir un producto al carrito después de registrar un nuevo usuario.
        """
        # --- Parte 1: Registro de Usuario ---
        self.home_page.goto()  # goto() ya espera que la página cargue
        self.home_page.navbar_horizontal.click_my_account_option("Register")
        
        unique_email = f"test.user.{int(time.time())}@example.com"
        self.register_page.register(
            firstname="Brayan",
            lastname="Mendoza",
            email=unique_email,
            telephone="+1234567890",
            password="Test@123",
            password_confirm="Test@123",
            subscribe_newsletter=True
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
        expect(self.page.locator(self.home_page.cart_panel.panel)).to_be_visible()
        
        # expect() con auto-wait
        cart_message = self.page.locator(self.home_page.cart_panel.message)
        expect(cart_message).not_to_be_visible()
        
        # Mejor usar expect() que text_content() para valores dinámicos
        sub_total_locator = self.page.locator(self.home_page.cart_panel.sub_total)
        total_locator = self.page.locator(self.home_page.cart_panel.total)
        
        # expect() espera automáticamente hasta que el texto no sea $0.00
        expect(sub_total_locator).not_to_have_text("$0.00")
        expect(total_locator).not_to_have_text("$0.00")

