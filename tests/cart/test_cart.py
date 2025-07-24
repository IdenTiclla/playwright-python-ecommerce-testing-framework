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


    def test_adding_product_to_cart_from_quick_view_modal(self):

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

        self.success_page.wait_for_page_load()

        cart_counter = self.home_page.header_actions.get_cart_count()
        assert cart_counter == "0"

        self.home_page.goto()
        self.home_page.top_products.show_quick_view(index=3)
        self.home_page.quick_view_modal.add_to_cart()

        expect(self.home_page.notification.container).to_be_visible()
        expected_message = "Success: You have added iMac to your shopping cart!"
        expect(self.home_page.notification.message).to_have_text(expected_message)

        expect(self.home_page.notification.view_cart_button).to_be_visible()
        expect(self.home_page.notification.checkout_button).to_be_visible()
        
        cart_counter = self.home_page.header_actions.get_cart_count()
        assert cart_counter == "1"

    def test_empty_shopping_cart_with_new_user(self):
        """
        Verifica que el carrito de compras está vacío para un usuario recién registrado.
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

        self.success_page.wait_for_page_load()

        self.home_page.goto()

        self.home_page.header_actions.click_on_cart_button()
        self.home_page.cart_panel.click_on_edit_cart_button()

        self.shopping_cart_page.wait_for_page_load()

        assert self.shopping_cart_page.get_page_title() == "Shopping Cart"
        assert self.shopping_cart_page.get_empty_cart_message() == "Your shopping cart is empty!"

    def test_shopping_cart_with_new_user_and_product_in_cart(self):
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

        self.success_page.wait_for_page_load()

        self.success_page.navbar_horizontal.click_home_page()
        
        self.home_page.wait_for_page_load()

        product_name = self.home_page.top_products.get_product_name(index=0)
        product_price = self.home_page.top_products.get_product_price(index=0)

        self.home_page.top_products.add_product_to_cart(index=0)

        self.home_page.header_actions.click_on_cart_button()
        self.home_page.cart_panel.click_on_edit_cart_button()

        self.shopping_cart_page.wait_for_page_load()

        quantity_of_products_on_shopping_cart = self.shopping_cart_page.get_quantity_of_products()
        assert quantity_of_products_on_shopping_cart == 1
        
        product_is_on_shopping_cart = self.shopping_cart_page.shopping_cart_contains_product(product_name)
        assert product_is_on_shopping_cart == True

        product_name_on_shopping_cart = self.shopping_cart_page.get_product_name(index=0)
        assert product_name in product_name_on_shopping_cart

        # Verificamos que el producto no está disponible en la cantidad deseada o no está en stock
        alert_messages = self.shopping_cart_page.alert_component.get_alert_messages()
        assert any("Products marked with *** are not available in the desired quantity or not in stock!" in alert_message for alert_message in alert_messages)

        product_quantity = self.shopping_cart_page.get_product_quantity(index=0)
        assert product_quantity == 1

        unit_price = self.shopping_cart_page.get_unit_price(index=0)
        assert unit_price == product_price

        total_price = self.shopping_cart_page.get_total_price(index=0)
        assert total_price == product_price

    def test_edit_quantity_of_product_in_shopping_cart(self):
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

        self.success_page.wait_for_page_load()

        self.success_page.navbar_horizontal.click_home_page()
        
        self.home_page.wait_for_page_load()

        product_price = self.home_page.top_products.get_product_price(index=0)

        self.home_page.top_products.add_product_to_cart(index=0)

        self.home_page.header_actions.click_on_cart_button()
        self.home_page.cart_panel.click_on_edit_cart_button()

        self.shopping_cart_page.wait_for_page_load()

        quantity_of_products_on_shopping_cart = self.shopping_cart_page.get_quantity_of_products()
        assert quantity_of_products_on_shopping_cart == 1

        unit_price = self.shopping_cart_page.get_unit_price(index=0)
        total_price = self.shopping_cart_page.get_total_price(index=0)
        assert product_price == unit_price
        assert total_price == unit_price * quantity_of_products_on_shopping_cart

        # Edit the quantity of the product in the shopping cart

        self.shopping_cart_page.edit_quantity_of_product(index=0, quantity=2)
        self.shopping_cart_page.wait_for_page_load()

        # get alert message after updating the quantity of the product
        alert_messages = self.shopping_cart_page.alert_component.get_alert_messages()
        print("alert_messages: ", alert_messages)
        # `assert "Success: You have modified your shopping cart!" in alert_text
        # assert "Success: You have modified your shopping cart!" in any(alert_txt for alert_txt in alert_texts)
        assert any("Success: You have modified your shopping cart!" in alert_message for alert_message in alert_messages)
        quantity_of_products_on_shopping_cart_updated = self.shopping_cart_page.get_product_quantity(index=0)
        assert quantity_of_products_on_shopping_cart_updated == 2

        unit_price = self.shopping_cart_page.get_unit_price(index=0)
        total_price = self.shopping_cart_page.get_total_price(index=0)
        assert product_price == unit_price
        assert total_price == unit_price * quantity_of_products_on_shopping_cart_updated

        print("product_price: ", product_price)
        print("unit_price: ", unit_price)
        print("quantity_of_products_on_shopping_cart_updated: ", quantity_of_products_on_shopping_cart_updated)
        print("total_price: ", total_price)

    def test_add_product_to_cart_from_search_results(self):
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

        self.success_page.wait_for_page_load()
        self.success_page.navbar_horizontal.click_home_page()

        self.home_page.search_bar.search("")

        self.search_page.wait_for_page_load()

        product_name = self.search_page.get_product_name(index=1) 
        product_price = self.search_page.get_product_price(index=1)

        self.search_page.add_product_to_cart(index=1)

        self.home_page.notification.click_on_view_cart_button()

        self.shopping_cart_page.wait_for_page_load()
        product_name_on_shopping_cart = self.shopping_cart_page.get_product_name(index=0)
        assert product_name in product_name_on_shopping_cart

        product_quantity = self.shopping_cart_page.get_product_quantity(index=0)
        unit_price = self.shopping_cart_page.get_unit_price(index=0)
        total_price = self.shopping_cart_page.get_total_price(index=0)

        assert product_quantity == 1
        assert unit_price == product_price
        assert total_price == unit_price * product_quantity

        self.shopping_cart_page.wait_for_page_load()

        self.shopping_cart_page.edit_quantity_of_product(index=0, quantity=2)

        product_quantity = self.shopping_cart_page.get_product_quantity(index=0)
        unit_price = self.shopping_cart_page.get_unit_price(index=0)
        total_price = self.shopping_cart_page.get_total_price(index=0)

        assert product_quantity == 2
        assert unit_price == product_price
        assert total_price == unit_price * product_quantity

        self.shopping_cart_page.wait_for_page_load()


        self.shopping_cart_page.edit_quantity_of_product(index=0, quantity=3)

        product_quantity = self.shopping_cart_page.get_product_quantity(index=0)
        unit_price = self.shopping_cart_page.get_unit_price(index=0)
        total_price = self.shopping_cart_page.get_total_price(index=0)


        assert product_quantity == 3
        assert unit_price == product_price
        assert total_price == unit_price * product_quantity
