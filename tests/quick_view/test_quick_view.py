from pages.home_page import HomePage
import pytest
from playwright.sync_api import expect
class TestQuickView:

    @pytest.fixture
    def home_page(self, page) -> HomePage:
        return HomePage(page)
    
    def test_quick_view(self, home_page, page):
        home_page.goto()
        home_page.top_products.scroll_to_top_products()
        page.wait_for_timeout(1000)

        expect(page.locator(home_page.top_products.section)).to_be_visible(timeout=10000)

        home_page.top_products.show_quick_view(index=0)

        page.wait_for_timeout(1000)
        quick_view_modal = home_page.quick_view_modal

        expect(page.locator(quick_view_modal.title)).to_be_visible(timeout=10000)
        expect(page.locator(quick_view_modal.title)).to_contain_text("iMac")
        assert quick_view_modal.get_title() == "iMac"

        expect(page.locator(quick_view_modal.availability)).to_be_visible(timeout=10000)
        expect(page.locator(quick_view_modal.availability)).to_contain_text("Out Of Stock")

        quick_view_modal.close()
        expect(page.locator(quick_view_modal.container)).to_be_hidden(timeout=10000)

    def test_quick_view_many_times(self, home_page, page):
        home_page.goto()
        page.wait_for_timeout(1000)

        home_page.top_products.scroll_to_top_products()
        page.wait_for_timeout(1000)

        expect(page.locator(home_page.top_products.section)).to_be_visible(timeout=10000)


        for i in range(4):
            print(f"Showing quick view {i+1}")
            home_page.top_products.show_quick_view(index=i)
            quick_view_modal = home_page.quick_view_modal
            expect(page.locator(quick_view_modal.container)).to_be_visible(timeout=10000)
            quick_view_modal.close()
            expect(page.locator(quick_view_modal.container)).to_be_hidden(timeout=10000)
            page.wait_for_timeout(1000)




