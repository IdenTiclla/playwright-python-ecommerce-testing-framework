from tests.base_test import BaseTest
from playwright.sync_api import expect
import time


class TestProduct(BaseTest):
    def test_first_carousel_product_availability(self):
        self.home_page.goto()
        self.home_page.carousel.slides.nth(0).click()
        assert self.product_page.get_product_availability() == "Out Of Stock"
    
    def test_second_carousel_product_availability(self):
        self.home_page.goto()
        self.home_page.carousel.navigate_to_next_slide()
        self.home_page.carousel.slides.nth(1).click()
        assert self.product_page.get_product_availability() == "Out Of Stock"
    
    def test_third_carousel_product_availability(self):
        self.home_page.goto()
        self.home_page.carousel.navigate_to_next_slide()
        self.home_page.carousel.navigate_to_next_slide()
        self.home_page.carousel.slides.nth(2).click()
        assert self.product_page.get_product_availability() == "In Stock"

    def test_default_quantity_on_product_page(self):
        self.home_page.goto()
        self.home_page.carousel.slides.nth(0).click()
        assert self.product_page.get_product_quantity() == 1

    def test_top_product_availability(self):
        self.home_page.goto()
        self.home_page.top_products.scroll_to_top_products()
        self.home_page.top_products.product_items.nth(0).click()
        url = self.product_page.page.url
        assert url == "https://ecommerce-playground.lambdatest.io/index.php?route=product/product&product_id=107"
        assert self.product_page.get_product_name() == "iMac"
        assert self.product_page.get_product_price() == "$170.00"
        assert self.product_page.get_product_availability() == "Out Of Stock"

    def test_increase_quantity_on_product_page(self):
        # Navigate to the home page and click on the first product in the carousel
        self.home_page.goto()
        self.home_page.carousel.slides.nth(0).click()
        self.product_page.wait_for_page_load()
        
        # Get the initial quantity of the product
        initial_quantity = self.product_page.get_product_quantity()

        # Increase the quantity of the product by 9
        for i in range(9):
            self.product_page.increase_product_quantity()
        
        # Get the final quantity of the product
        final_quantity = self.product_page.get_product_quantity()
        
        # Assert that the final quantity is the initial quantity plus 9
        assert final_quantity == initial_quantity + 9

    def test_decrease_limit_on_product_page(self):
        self.home_page.goto()
        self.home_page.carousel.slides.nth(0).click()
        self.product_page.wait_for_page_load()

        # Get initial quantity of the product
        initial_quantity = self.product_page.get_product_quantity()

        # Decrease the quantity of the product by 9
        for i in range(9):
            self.product_page.decrease_product_quantity()

        # Get final quantity of the product
        final_quantity = self.product_page.get_product_quantity()

        # Assert that the final quantity is the initial quantity
        assert final_quantity == initial_quantity

    def test_increase_and_decrease_quantity_on_product_page(self):
        # Navigate to the home page and click on the first product in the carousel
        self.home_page.goto()
        self.home_page.carousel.slides.nth(0).click()
        self.product_page.wait_for_page_load()

        # Get initial quantity of the product
        initial_quantity = self.product_page.get_product_quantity()
        
        # Increase the product's quantity by 9
        for i in range(9):
            self.product_page.increase_product_quantity()

        # Get final product's quantity
        final_quantity = self.product_page.get_product_quantity()

        # Assert that the final quantity is the initial quantity plus 9
        assert final_quantity == initial_quantity + 9
        
        # Decrease the product's quantity by 9
        for i in range(9):
            self.product_page.decrease_product_quantity()

        # Get final product's quantity
        final_quantity = self.product_page.get_product_quantity()

        # Assert that the final quantity is the initial quantity
        assert final_quantity == initial_quantity