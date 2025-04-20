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
        
        # count = search_page.page.locator(search_page.product_titles).count()
        # assert count > 0, "Expected at least one search result"
        
        search_page.page.wait_for_load_state("domcontentloaded")
        # search_page.page.wait_for_selector(search_page.product_titles, timeout=10000)
        count = search_page.page.locator(search_page.product_titles).count()
        assert count > 0, "Expected at least one search result"


        results = search_page.get_search_results()
        assert any("iMac" in title for title in results), "Expected to find iMac in search results"

    def test_search_no_results(self, search_page: SearchPage, home_page: HomePage):
        home_page.goto()
        search_page.perform_search("xyzabc123nonexistent")
        expect(search_page.page.locator(search_page.no_results_message)).to_be_visible()
        assert not search_page.has_results(), "Expected to find no results"

    def test_search_with_category(self, search_page: SearchPage, home_page: HomePage):
        home_page.goto()
        search_page.perform_search("iMac", category="Desktops")
        count = search_page.page.locator(search_page.product_titles).count()
        assert count > 0, "Expected at least one search result"
        results = search_page.get_search_results()
        assert any("iMac" in title for title in results), "Expected to find iMac in search results"