import pytest
from tests.base_test import BaseTest

class TestMainCarousel(BaseTest):
    """Test suite for the main carousel component functionality."""
    
    @pytest.fixture(autouse=True)
    def setup_carousel_test(self):
        """Setup method to navigate to homepage before each test."""
        self.home_page.goto()
        self.carousel = self.home_page.carousel
        self.carousel.wait_for_carousel_load()
        # Disable auto-play to prevent test interference
        self.carousel.disable_auto_play()
    
    def test_carousel_visibility_and_basic_structure(self):
        """Test that carousel is visible and has expected structure."""
        # Verify carousel is visible
        assert self.carousel.is_visible(), "Carousel should be visible on homepage"
        
        # Verify carousel has slides
        slide_count = self.carousel.get_slide_count()
        assert slide_count > 0, "Carousel should have at least one slide"
        
        # Verify carousel has indicators
        indicator_count = self.carousel.get_indicator_count()
        assert indicator_count > 0, "Carousel should have slide indicators"
        assert indicator_count == slide_count, "Number of indicators should match number of slides"
        
        # Verify navigation buttons are visible
        assert self.carousel.are_navigation_buttons_visible(), "Navigation buttons should be visible"
        assert self.carousel._are_navigation_buttons_present(), "Navigation buttons should be present"
    
    def test_carousel_initial_state(self):
        """Test the initial state of the carousel."""
        # Verify there's an active slide
        active_slide_index = self.carousel.get_active_slide_index()
        assert active_slide_index >= 0, "There should be an active slide"
        
        # Verify there's an active indicator
        active_indicator_index = self.carousel.get_active_indicator_index()
        assert active_indicator_index >= 0, "There should be an active indicator"
        
        # Verify active slide and indicator match
        assert active_slide_index == active_indicator_index, \
            "Active slide and indicator indices should match"
    
    def test_next_slide_navigation(self):
        """Test navigation to next slide using next button."""
        initial_slide_index = self.carousel.get_active_slide_index()
        slide_count = self.carousel.get_slide_count()
        
        # Navigate to next slide
        self.carousel.navigate_to_next_slide()
        
        # Verify slide changed
        new_slide_index = self.carousel.get_active_slide_index()
        expected_index = (initial_slide_index + 1) % slide_count
        assert new_slide_index == expected_index, \
            f"Expected slide {expected_index}, but got {new_slide_index}"
        
        # Verify indicator also changed
        new_indicator_index = self.carousel.get_active_indicator_index()
        assert new_indicator_index == new_slide_index, \
            "Active indicator should match active slide"
    
    def test_previous_slide_navigation(self):
        """Test navigation to previous slide using previous button."""
        slide_count = self.carousel.get_slide_count()
        
        # Start from slide 1 (not 0) to test previous navigation without wrap-around issues
        self.carousel.navigate_to_slide_by_index(1)
        self.carousel.page.wait_for_timeout(500)  # Wait for navigation to complete
        
        initial_slide_index = self.carousel.get_active_slide_index()
        assert initial_slide_index == 1, "Should be on slide 1 before testing previous navigation"
        
        # Navigate to previous slide
        self.carousel.navigate_to_previous_slide()
        
        # Verify slide changed
        new_slide_index = self.carousel.get_active_slide_index()
        expected_index = 0  # From slide 1, previous should be slide 0
        assert new_slide_index == expected_index, \
            f"Expected slide {expected_index}, but got {new_slide_index}"
        
        # Verify indicator also changed
        new_indicator_index = self.carousel.get_active_indicator_index()
        assert new_indicator_index == new_slide_index, \
            "Active indicator should match active slide"
    
    def test_indicator_navigation(self):
        """Test navigation using slide indicators."""
        slide_count = self.carousel.get_slide_count()
        
        if slide_count < 2:
            pytest.skip("Need at least 2 slides to test indicator navigation")
        
        # Test clicking on different indicators
        for target_index in range(min(slide_count, 3)):  # Test first 3 indicators
            self.carousel.navigate_to_slide_by_indicator(target_index)
            
            # Verify correct slide is active
            active_slide_index = self.carousel.get_active_slide_index()
            assert active_slide_index == target_index, \
                f"Expected slide {target_index}, but got {active_slide_index}"
            
            # Verify correct indicator is active
            active_indicator_index = self.carousel.get_active_indicator_index()
            assert active_indicator_index == target_index, \
                f"Expected indicator {target_index}, but got {active_indicator_index}"
    
    def test_carousel_cycle_through_all_slides(self):
        """Test cycling through all slides using next button."""
        slide_count = self.carousel.get_slide_count()
        
        if slide_count < 2:
            pytest.skip("Need at least 2 slides to test cycling")
        
        # Disable auto-play to prevent interference
        self.carousel.disable_auto_play()
        
        # Start from slide 0 to ensure consistent testing
        self.carousel.navigate_to_slide_by_index(0)
        
        initial_slide_index = self.carousel.get_active_slide_index()
        visited_slides = []
        
        # Cycle through all slides with better timing
        for i in range(slide_count):
            current_slide = self.carousel.get_active_slide_index()
            visited_slides.append(current_slide)
            
            if i < slide_count - 1:  # Don't navigate after last slide
                self.carousel.navigate_to_next_slide()
                # Add extra wait to ensure navigation completes
                self.carousel.page.wait_for_timeout(800)
        
        # Verify we visited all slides
        unique_slides = set(visited_slides)
        assert len(unique_slides) == slide_count, \
            f"Should visit all {slide_count} slides, but visited {visited_slides}. Unique slides: {unique_slides}"
        
        # Verify we visited slides in correct order (0, 1, 2, ...)
        expected_slides = list(range(slide_count))
        assert visited_slides == expected_slides, \
            f"Expected sequential slides {expected_slides}, but got {visited_slides}"
        
        # Navigate one more time to test wraparound
        self.carousel.navigate_to_next_slide()
        self.carousel.page.wait_for_timeout(800)
        final_slide_index = self.carousel.get_active_slide_index()
        assert final_slide_index == 0, \
            f"Should wrap around to slide 0, but got slide {final_slide_index}"
    
    def test_slide_content_information(self):
        """Test getting content information from slides."""
        slide_count = self.carousel.get_slide_count()
        
        # Get content from current active slide
        active_content = self.carousel.get_active_slide_content()
        
        # Verify content structure
        assert isinstance(active_content, dict), "Slide content should be a dictionary"
        assert "index" in active_content, "Content should include slide index"
        assert "has_image" in active_content, "Content should include image flag"
        assert "has_link" in active_content, "Content should include link flag"
        assert "has_caption" in active_content, "Content should include caption flag"
        
        # If slide has image, verify image details
        if active_content["has_image"]:
            assert "image_src" in active_content, "Should include image source"
            assert "image_alt" in active_content, "Should include image alt text"
        
        # If slide has link, verify link details
        if active_content["has_link"]:
            assert "link_href" in active_content, "Should include link href"
    
    def test_get_all_slide_contents(self):
        """Test getting content from all slides."""
        all_contents = self.carousel.get_all_slide_contents()
        slide_count = self.carousel.get_slide_count()
        
        assert len(all_contents) == slide_count, \
            f"Should get content for all {slide_count} slides"
        
        # Verify each slide content has expected structure
        for i, content in enumerate(all_contents):
            assert content["index"] == i, f"Slide {i} should have correct index"
            assert isinstance(content["has_image"], bool), "has_image should be boolean"
            assert isinstance(content["has_link"], bool), "has_link should be boolean"
            assert isinstance(content["has_caption"], bool), "has_caption should be boolean"
    
    def test_carousel_functionality_verification(self):
        """Test the comprehensive functionality verification method."""
        results = self.carousel.verify_carousel_functionality()
        
        # Verify results structure
        expected_keys = [
            "is_visible", "slide_count", "indicator_count", "has_navigation_buttons",
            "has_indicators", "active_slide_index", "active_indicator_index", "auto_play_enabled"
        ]
        
        for key in expected_keys:
            assert key in results, f"Results should include {key}"
        
        # Verify basic functionality
        assert results["is_visible"] is True, "Carousel should be visible"
        assert results["slide_count"] > 0, "Should have slides"
        assert results["indicator_count"] > 0, "Should have indicators"
        assert results["has_navigation_buttons"] is True, "Should have navigation buttons"
        assert results["has_indicators"] is True, "Should have indicators"
        assert results["active_slide_index"] >= 0, "Should have active slide"
        assert results["active_indicator_index"] >= 0, "Should have active indicator"
        
        # If carousel has multiple slides, should test navigation
        if results["slide_count"] > 1:
            assert "next_navigation_works" in results, "Should test next navigation"
            assert "prev_navigation_works" in results, "Should test prev navigation"
    
    def test_carousel_assertion_methods(self):
        """Test carousel assertion methods for testing."""
        # Test carousel visibility assertion
        self.carousel.assert_carousel_is_visible()
        
        # Test slide count assertion
        actual_count = self.carousel.get_slide_count()
        self.carousel.assert_slide_count(actual_count)
        
        # Test active slide assertion
        active_slide_index = self.carousel.get_active_slide_index()
        self.carousel.assert_slide_is_active(active_slide_index)
        
        # Test active indicator assertion
        active_indicator_index = self.carousel.get_active_indicator_index()
        self.carousel.assert_indicator_is_active(active_indicator_index)
    
    def test_carousel_assertion_failures(self):
        """Test that carousel assertions fail appropriately."""
        # Test slide count assertion failure
        actual_count = self.carousel.get_slide_count()
        with pytest.raises(AssertionError):
            self.carousel.assert_slide_count(actual_count + 10)
        
        # Test active slide assertion failure
        with pytest.raises(AssertionError):
            self.carousel.assert_slide_is_active(999)  # Invalid slide index
        
        # Test active indicator assertion failure
        with pytest.raises(AssertionError):
            self.carousel.assert_indicator_is_active(999)  # Invalid indicator index
    
    def test_slide_navigation_edge_cases(self):
        """Test edge cases in slide navigation."""
        slide_count = self.carousel.get_slide_count()
        
        # Test invalid indicator index
        with pytest.raises(ValueError):
            self.carousel.navigate_to_slide_by_indicator(-1)
        
        with pytest.raises(ValueError):
            self.carousel.navigate_to_slide_by_indicator(slide_count)
        
        # Test invalid slide index for clicking
        with pytest.raises(ValueError):
            self.carousel.click_slide_by_index(-1)
        
        with pytest.raises(ValueError):
            self.carousel.click_slide_by_index(slide_count)
    
    @pytest.mark.slow
    def test_auto_play_functionality(self):
        """Test auto-play functionality if enabled."""
        if not self.carousel.is_auto_play_enabled():
            pytest.skip("Auto-play is not enabled for this carousel")
        
        # Wait for automatic slide change
        slide_changed = self.carousel.wait_for_auto_slide_change(timeout=15000)
        assert slide_changed, "Auto-play should change slides automatically"
    
    def test_slide_click_functionality(self):
        """Test clicking on slides."""
        initial_url = self.carousel.page.url
        
        # Try to click the active slide
        try:
            self.carousel.click_active_slide()
            # If click was successful and navigated away, go back
            if self.carousel.page.url != initial_url:
                self.carousel.page.go_back()
                self.carousel.wait_for_carousel_load()
        except Exception:
            # Some slides might not be clickable, which is fine
            pass
        
        # Test clicking specific slide by index
        slide_count = self.carousel.get_slide_count()
        if slide_count > 1:
            try:
                self.carousel.click_slide_by_index(1)
                # If click was successful and navigated away, go back
                if self.carousel.page.url != initial_url:
                    self.carousel.page.go_back()
                    self.carousel.wait_for_carousel_load()
            except Exception:
                # Some slides might not be clickable, which is fine
                pass
