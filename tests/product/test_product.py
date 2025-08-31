from tests.base_test import BaseTest
from playwright.sync_api import expect


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
        