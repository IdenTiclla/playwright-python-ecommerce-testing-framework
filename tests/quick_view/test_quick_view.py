import pytest
from playwright.sync_api import expect
from tests.base_test import BaseTest

@pytest.mark.quick_view_modal
class TestQuickView(BaseTest):

    def test_quick_view_with_out_of_stock_product(self):
        self.home_page.goto()
        self.home_page.top_products.scroll_to_top_products()
        self.page.wait_for_timeout(1000)

        expect(self.page.locator(self.home_page.top_products.section)).to_be_visible(timeout=10000)

        self.home_page.top_products.show_quick_view(index=0)

        self.page.wait_for_timeout(1000)
        quick_view_modal = self.home_page.quick_view_modal

        expect(self.page.locator(quick_view_modal.title)).to_be_visible(timeout=10000)
        expect(self.page.locator(quick_view_modal.title)).to_contain_text("iMac")
        assert quick_view_modal.get_title() == "iMac"

        expect(self.page.locator(quick_view_modal.availability)).to_be_visible(timeout=10000)
        expect(self.page.locator(quick_view_modal.availability)).to_contain_text("Out Of Stock")

        quick_view_modal.close()
        expect(self.page.locator(quick_view_modal.container)).to_be_hidden(timeout=10000)

        add_to_cart_button_text = quick_view_modal.get_add_to_cart_button_text()
        buy_now_button_text = quick_view_modal.get_buy_now_button_text()
        assert add_to_cart_button_text == "Out Of Stock", "Add to Cart button text should be 'Out Of Stock'"
        assert buy_now_button_text == "Out Of Stock", "Buy Now button text should be 'Out Of Stock'"

    def test_quick_view_many_times(self):
        self.home_page.goto()
        self.page.wait_for_timeout(1000)

        self.home_page.top_products.scroll_to_top_products()
        self.page.wait_for_timeout(1000)

        expect(self.page.locator(self.home_page.top_products.section)).to_be_visible(timeout=10000)


        for i in range(4):
            print(f"Showing quick view {i+1}")
            self.home_page.top_products.show_quick_view(index=i)
            quick_view_modal = self.home_page.quick_view_modal
            expect(self.page.locator(quick_view_modal.container)).to_be_visible(timeout=10000)
            quick_view_modal.close()
            expect(self.page.locator(quick_view_modal.container)).to_be_hidden(timeout=10000)
            self.page.wait_for_timeout(1000)


    def test_quick_view_with_in_stock_product(self):
        self.home_page.goto()
        self.page.wait_for_timeout(1000)

        self.home_page.top_products.scroll_to_top_products()
        self.page.wait_for_timeout(1000)
        
        expect(self.page.locator(self.home_page.top_products.section)).to_be_visible(timeout=10000)

        self.home_page.top_products.show_quick_view(index=2)
        self.page.wait_for_timeout(1000)

        quick_view_modal = self.home_page.quick_view_modal
        expect(self.page.locator(quick_view_modal.container)).to_be_visible(timeout=10000)
        expect(self.page.locator(quick_view_modal.title)).to_be_visible(timeout=10000)
        expect(self.page.locator(quick_view_modal.title)).to_contain_text("iMac")
        assert quick_view_modal.get_title() == "iMac"

        expect(self.page.locator(quick_view_modal.availability)).to_be_visible(timeout=10000)
        expect(self.page.locator(quick_view_modal.availability)).to_contain_text("In Stock")

        add_to_cart_button_text = quick_view_modal.get_add_to_cart_button_text()
        buy_now_button_text = quick_view_modal.get_buy_now_button_text()
        assert add_to_cart_button_text == "Add to Cart", "Add to Cart button text should be 'Add to Cart'"
        assert buy_now_button_text == "Buy now", "Buy Now button text should be 'Buy now'"

        quick_view_modal.close()
        expect(self.page.locator(quick_view_modal.container)).to_be_hidden(timeout=10000)
        




