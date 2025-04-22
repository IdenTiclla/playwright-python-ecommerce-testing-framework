import pytest
from pages.home_page import HomePage
from playwright.sync_api import expect

class TestHomePage:
    @pytest.fixture
    def home_page(self, page):
        return HomePage(page)

    def test_specific_carousel_visible_and_slides(self, home_page):
        home_page.goto()
        # Check specific carousel is visible
        assert home_page.carousel.is_visible(), "#mz-carousel-217960 should be visible on homepage"
        # Check there is more than one slide
        slide_count = home_page.carousel.get_slide_count()
        assert slide_count > 1, f"Expected more than one slide, got {slide_count}"
        # Check navigation: go to next slide and verify active slide changes
        initial_index = home_page.carousel.get_active_slide_index()
        assert initial_index == 0
        home_page.carousel.go_to_next_slide()
        home_page.page.wait_for_timeout(1000)
        new_index = home_page.carousel.get_active_slide_index()
        assert new_index == 1

        home_page.carousel.go_to_next_slide()
        home_page.page.wait_for_timeout(1000)
        new_index = home_page.carousel.get_active_slide_index()
        assert new_index == 2

        assert new_index != initial_index, "Carousel should move to next slide when next is clicked"
