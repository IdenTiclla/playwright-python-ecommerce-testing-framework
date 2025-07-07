import pytest
from pages.search_page import SearchPage
from pages.home_page import HomePage
from playwright.sync_api import Page, expect

class TestSearch:
    @pytest.fixture
    def search_page(self, page: Page) -> SearchPage:
        return SearchPage(page)
    
    @pytest.fixture
    def home_page(self, page: Page) -> HomePage:
        return HomePage(page)

    def test_search_functionality(self, search_page: SearchPage, home_page: HomePage):
        home_page.goto()
        search_page.perform_search("iMac")

        expect(search_page.product_items).to_have_count(8)
        
        results = search_page.get_search_results()
        assert any("iMac" in title for title in results), "Expected to find iMac in search results"


    def test_search_iphone(self, search_page: SearchPage, home_page: HomePage):
        home_page.goto()
        search_page.perform_search("iPhone")

        expect(search_page.product_items).to_have_count(4)

    def test_search_no_results(self, search_page: SearchPage, home_page: HomePage):
        home_page.goto()
        search_page.perform_search("xyzabc123nonexistent")
        
        expect(search_page.no_results_message).to_be_visible()
        assert not search_page.has_results(), "Expected to find no results"

    def test_search_with_results(self, search_page: SearchPage, home_page: HomePage):
        home_page.goto()
        search_page.perform_search("iPod")
        
        expect(search_page.product_items).to_have_count(15)
        assert search_page.has_results(), "Expected to find results"
        
        results = search_page.get_search_results()
        assert any("iPod" in title for title in results), "Expected to find iPod in search results"

    def test_search_with_category(self, search_page: SearchPage, home_page: HomePage):
        home_page.goto()
        search_page.perform_search("iMac", category="Desktops", search_in_description=True)
        
        # Ensure we have at least one result by checking first product is visible
        expect(search_page.product_items.first).to_be_visible()
        count = search_page.get_result_count()
        assert count > 0, "Expected at least one search result"
        
        results = search_page.get_search_results()
        assert any("iMac" in title for title in results), "Expected to find iMac in search results"

    def test_search_results_sorting_by_price_low_to_high(self, search_page: SearchPage, home_page: HomePage):
        home_page.goto()
        search_page.perform_search("iPod")
        
        # Ensure we have results to sort by checking first product is visible
        expect(search_page.product_items.first).to_be_visible()
        count = search_page.get_result_count()
        assert count > 0, "Expected at least one search result"
        
        results = search_page.get_search_results()
        assert any("iPod" in title for title in results), "Expected to find iPod in search results"

        search_page.sort_by_price_low_to_high()
        # assert url contains order=ASC
        assert "order=ASC" in search_page.page.url, "Expected to find order=ASC in url"

        assert search_page.check_if_sorted_by_price_low_to_high(), "Expected to be sorted by price low to high"

    def test_search_results_sorting_by_price_high_to_low(self, search_page: SearchPage, home_page: HomePage):
        home_page.goto()
        search_page.perform_search("iPod")
        
        # Ensure we have results to sort by checking first product is visible
        expect(search_page.product_items.first).to_be_visible()
        count = search_page.get_result_count()
        assert count > 0, "Expected at least one search result"

        search_page.sort_by_price_high_to_low()
        # assert url contains order=DESC
        assert "order=DESC" in search_page.page.url, "Expected to find order=DESC in url"

        assert search_page.check_if_sorted_by_price_high_to_low(), "Expected to be sorted by price high to low"