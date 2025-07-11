
from pages.search_page import SearchPage
from pages.home_page import HomePage
from playwright.sync_api import expect
from tests.base_test import BaseTest
class TestSearch(BaseTest):

    def test_search_functionality(self):
        self.home_page.goto()
        self.search_page.perform_search("iMac")

        expect(self.search_page.product_items).to_have_count(8)
        
        results = self.search_page.get_search_results()
        assert any("iMac" in title for title in results), "Expected to find iMac in search results"


    def test_search_iphone(self):
        self.home_page.goto()
        self.search_page.perform_search("iPhone")

        expect(self.search_page.product_items).to_have_count(4)

    def test_search_no_results(self):
        self.home_page.goto()
        self.search_page.perform_search("xyzabc123nonexistent")
        
        expect(self.search_page.no_results_message).to_be_visible()
        assert not self.search_page.has_results(), "Expected to find no results"

    def test_search_with_results(self):
        self.home_page.goto()
        self.search_page.perform_search("iPod")
        
        expect(self.search_page.product_items).to_have_count(15)
        assert self.search_page.has_results(), "Expected to find results"
        
        results = self.search_page.get_search_results()
        assert any("iPod" in title for title in results), "Expected to find iPod in search results"

    def test_search_with_category(self):
        self.home_page.goto()
        self.search_page.perform_search("iMac", category="Desktops", search_in_description=True)
        
        # Ensure we have at least one result by checking first product is visible
        expect(self.search_page.product_items.first).to_be_visible()
        count = self.search_page.get_result_count()
        assert count > 0, "Expected at least one search result"
        
        results = self.search_page.get_search_results()
        assert any("iMac" in title for title in results), "Expected to find iMac in search results"

    def test_search_results_sorting_by_price_low_to_high(self):
        self.home_page.goto()
        self.search_page.perform_search("iPod")
        
        # Ensure we have results to sort by checking first product is visible
        expect(self.search_page.product_items.first).to_be_visible()
        count = self.search_page.get_result_count()
        assert count > 0, "Expected at least one search result"
        
        results = self.search_page.get_search_results()
        assert any("iPod" in title for title in results), "Expected to find iPod in search results"

        self.search_page.sort_by_price_low_to_high()
        # assert url contains order=ASC
        assert "order=ASC" in self.search_page.page.url, "Expected to find order=ASC in url"

        assert self.search_page.check_if_sorted_by_price_low_to_high(), "Expected to be sorted by price low to high"

    def test_search_results_sorting_by_price_high_to_low(self):
        self.home_page.goto()
        self.search_page.perform_search("iPod")
        
        # Ensure we have results to sort by checking first product is visible
        expect(self.search_page.product_items.first).to_be_visible()
        count = self.search_page.get_result_count()
        assert count > 0, "Expected at least one search result"

        self.search_page.sort_by_price_high_to_low()
        # assert url contains order=DESC
        assert "order=DESC" in self.search_page.page.url, "Expected to find order=DESC in url"

        assert self.search_page.check_if_sorted_by_price_high_to_low(), "Expected to be sorted by price high to low"