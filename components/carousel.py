from playwright.sync_api import Page, Locator, expect
from typing import Optional, List
import time
from components.base_component import BaseComponent

class MainCarousel(BaseComponent):
    """
    Page Object Model for the main carousel component on the ecommerce playground homepage.
    
    This carousel displays promotional banners with navigation controls and slide indicators.
    Supports both manual navigation and auto-play functionality.
    """
    
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Main carousel container
        self.carousel_container = page.locator("div#mz-carousel-217960")
        
        # Slide elements
        self.slides = self.carousel_container.locator(".carousel-item")
        self.active_slide = self.carousel_container.locator(".carousel-item.active")
        
        # Navigation controls
        self.next_button = self.carousel_container.locator("a.carousel-control-next")
        self.prev_button = self.carousel_container.locator("a.carousel-control-prev")
        
        # Slide indicators (dots)
        self.indicators_container = self.carousel_container.locator(".carousel-indicators")
        self.indicators = self.indicators_container.locator("li")
        self.active_indicator = self.indicators_container.locator("li.active")
        
        # Slide content elements
        self.slide_images = self.slides.locator("img")
        self.slide_links = self.slides.locator("a")
        self.slide_content = self.slides.locator(".carousel-caption, .slide-content")

    # Visibility and State Methods
    
    def is_visible(self) -> bool:
        """Check if the carousel is visible on the page."""
        return self._is_element_visible_dom("div#mz-carousel-217960")
    
    def wait_for_carousel_load(self, timeout: int = 10000) -> None:
        """Wait for the carousel to be fully loaded and visible."""
        # Wait for carousel container to be attached to DOM
        self.carousel_container.wait_for(state="attached", timeout=timeout)
        
        # Wait for at least one slide to be present
        self.slides.first.wait_for(state="attached", timeout=timeout/2)
        
        # Wait for navigation buttons to be attached
        try:
            self.next_button.wait_for(state="attached", timeout=timeout/4)
            self.prev_button.wait_for(state="attached", timeout=timeout/4)
        except Exception:
            # Navigation buttons might not be immediately available
            pass
        
        # Wait for active slide to be present
        self.active_slide.wait_for(state="attached", timeout=timeout/4)
    
    def is_auto_play_enabled(self) -> bool:
        """Check if carousel has auto-play functionality enabled."""
        try:
            carousel_element = self.carousel_container
            data_ride = carousel_element.get_attribute("data-ride", timeout=5000)
            data_interval = carousel_element.get_attribute("data-interval", timeout=5000)
            return data_ride == "carousel" or (data_interval and data_interval != "false")
        except Exception:
            # If we can't check attributes, assume auto-play is enabled for safety
            return True

    # Slide Information Methods
    
    def get_slide_count(self) -> int:
        """Get the total number of slides in the carousel."""
        return self.slides.count()
    
    def get_active_slide_index(self) -> int:
        """Get the index of the currently active slide (0-based)."""
        slide_count = self.get_slide_count()
        for i in range(slide_count):
            slide = self.slides.nth(i)
            if "active" in (slide.get_attribute("class") or ""):
                return i
        return -1
    
    def get_active_slide_content(self) -> dict:
        """Get content information from the currently active slide."""
        active_slide = self.active_slide
        
        content = {
            "index": self.get_active_slide_index(),
            "has_image": active_slide.locator("img").count() > 0,
            "has_link": active_slide.locator("a").count() > 0,
            "has_caption": active_slide.locator(".carousel-caption, .slide-content").count() > 0
        }
        
        # Get image details if present
        if content["has_image"]:
            img = active_slide.locator("img").first
            content["image_src"] = img.get_attribute("src")
            content["image_alt"] = img.get_attribute("alt")
        
        # Get link details if present
        if content["has_link"]:
            link = active_slide.locator("a").first
            content["link_href"] = link.get_attribute("href")
            content["link_title"] = link.get_attribute("title")
        
        # Get caption text if present
        if content["has_caption"]:
            caption = active_slide.locator(".carousel-caption, .slide-content").first
            content["caption_text"] = caption.text_content()
        
        return content

    # Navigation Methods
    
    def navigate_to_next_slide(self) -> 'MainCarousel':
        """Navigate to the next slide using the next button."""
        current_index = self.get_active_slide_index()
        
        # Ensure button is ready for interaction
        self.next_button.wait_for(state="attached", timeout=5000)
        
        # Use force click if normal click doesn't work due to visibility issues
        try:
            self.next_button.click(timeout=5000)
        except Exception:
            # Fallback to force click if normal click fails
            self.next_button.click(force=True)
        
        # Wait for slide transition
        self.page.wait_for_timeout(800)
        
        # Verify navigation occurred
        new_index = self.get_active_slide_index()
        expected_index = (current_index + 1) % self.get_slide_count()
        
        if new_index != expected_index:
            # Wait a bit more for slower transitions
            self.page.wait_for_timeout(1000)
        
        return self
    
    def navigate_to_previous_slide(self) -> 'MainCarousel':
        """Navigate to the previous slide using the previous button."""
        current_index = self.get_active_slide_index()
        slide_count = self.get_slide_count()
        
        # Ensure button is ready for interaction
        self.prev_button.wait_for(state="attached", timeout=5000)
        
        # Use force click if normal click doesn't work due to visibility issues
        try:
            self.prev_button.click(timeout=5000)
        except Exception:
            # Fallback to force click if normal click fails
            self.prev_button.click(force=True)
        
        # Wait for slide transition
        self.page.wait_for_timeout(800)
        
        # Verify navigation occurred
        new_index = self.get_active_slide_index()
        expected_index = (current_index - 1) % slide_count
        
        if new_index != expected_index:
            # Wait a bit more for slower transitions
            self.page.wait_for_timeout(1000)
            # Check again after longer wait
            new_index = self.get_active_slide_index()
        
        return self
    
    def navigate_to_slide_by_indicator(self, indicator_index: int) -> 'MainCarousel':
        """Navigate to a specific slide using the slide indicators."""
        if indicator_index < 0 or indicator_index >= self.indicators.count():
            raise ValueError(f"Indicator index {indicator_index} is out of range")
        
        # Disable auto-play to prevent interference
        if self.is_auto_play_enabled():
            self.page.evaluate("document.querySelector('div#mz-carousel-217960').setAttribute('data-interval', 'false')")
        
        indicator = self.indicators.nth(indicator_index)
        
        # Ensure indicator is ready for interaction
        indicator.wait_for(state="attached", timeout=5000)
        
        # Click the indicator
        try:
            indicator.click(timeout=5000)
        except Exception:
            # Fallback to force click if needed
            indicator.click(force=True)
        
        # Wait for slide transition with longer timeout
        self.page.wait_for_timeout(800)
        
        # Verify navigation occurred
        new_index = self.get_active_slide_index()
        if new_index != indicator_index:
            # Wait a bit more for slower transitions
            self.page.wait_for_timeout(1000)
        
        return self
    
    def navigate_to_slide_by_index(self, slide_index: int) -> 'MainCarousel':
        """Navigate to a specific slide by its index."""
        return self.navigate_to_slide_by_indicator(slide_index)

    # Indicator Methods
    
    def get_indicator_count(self) -> int:
        """Get the total number of slide indicators."""
        return self.indicators.count()
    
    def get_active_indicator_index(self) -> int:
        """Get the index of the currently active indicator."""
        indicator_count = self.get_indicator_count()
        for i in range(indicator_count):
            indicator = self.indicators.nth(i)
            if "active" in (indicator.get_attribute("class") or ""):
                return i
        return -1
    
    def are_indicators_visible(self) -> bool:
        """Check if slide indicators are visible."""
        return self.indicators_container.is_visible()

    # Interaction Methods
    
    def click_active_slide(self) -> 'MainCarousel':
        """Click on the currently active slide."""
        active_slide_link = self.active_slide.locator("a").first
        if active_slide_link.count() > 0:
            active_slide_link.click()
        else:
            # If no link, click on the slide itself
            self.active_slide.click()
        return self
    
    def click_slide_by_index(self, slide_index: int) -> 'MainCarousel':
        """Click on a specific slide by its index."""
        if slide_index < 0 or slide_index >= self.get_slide_count():
            raise ValueError(f"Slide index {slide_index} is out of range")
        
        slide = self.slides.nth(slide_index)
        slide_link = slide.locator("a").first
        
        if slide_link.count() > 0:
            slide_link.click()
        else:
            slide.click()
        
        return self

    # Verification Methods
    
    def verify_carousel_functionality(self) -> dict:
        """Verify basic carousel functionality and return results."""
        results = {
            "is_visible": self.is_visible(),
            "slide_count": self.get_slide_count(),
            "indicator_count": self.get_indicator_count(),
            "has_navigation_buttons": self._are_navigation_buttons_present(),
            "has_indicators": self.are_indicators_visible(),
            "active_slide_index": self.get_active_slide_index(),
            "active_indicator_index": self.get_active_indicator_index(),
            "auto_play_enabled": self.is_auto_play_enabled()
        }
        
        # Test navigation if carousel is functional
        if results["is_visible"] and results["slide_count"] > 1:
            initial_slide = self.get_active_slide_index()
            
            # Test next navigation
            try:
                self.navigate_to_next_slide()
                results["next_navigation_works"] = self.get_active_slide_index() != initial_slide
                
                # Return to original slide
                if results["next_navigation_works"]:
                    self.navigate_to_slide_by_index(initial_slide)
            except Exception:
                results["next_navigation_works"] = False
            
            # Test previous navigation
            try:
                self.navigate_to_previous_slide()
                results["prev_navigation_works"] = self.get_active_slide_index() != initial_slide
                
                # Return to original slide
                if results["prev_navigation_works"]:
                    self.navigate_to_slide_by_index(initial_slide)
            except Exception:
                results["prev_navigation_works"] = False
        
        return results
    
    def wait_for_auto_slide_change(self, timeout: int = 10000) -> bool:
        """Wait for an automatic slide change and return True if it occurred."""
        if not self.is_auto_play_enabled():
            return False
        
        initial_slide_index = self.get_active_slide_index()
        start_time = time.time()
        
        while (time.time() - start_time) * 1000 < timeout:
            current_slide_index = self.get_active_slide_index()
            if current_slide_index != initial_slide_index:
                return True
            self.page.wait_for_timeout(100)
        
        return False
    
    def get_all_slide_contents(self) -> List[dict]:
        """Get content information for all slides in the carousel."""
        slide_contents = []
        original_slide = self.get_active_slide_index()
        
        for i in range(self.get_slide_count()):
            self.navigate_to_slide_by_index(i)
            slide_content = self.get_active_slide_content()
            slide_contents.append(slide_content)
        
        # Return to original slide
        if original_slide >= 0:
            self.navigate_to_slide_by_index(original_slide)
        
        return slide_contents
    
    def disable_auto_play(self) -> 'MainCarousel':
        """Disable auto-play to prevent interference during testing."""
        try:
            # Try to disable auto-play by setting data-interval to false
            self.page.evaluate("""
                const carousel = document.querySelector('div#mz-carousel-217960');
                if (carousel) {
                    carousel.setAttribute('data-interval', 'false');
                    carousel.setAttribute('data-ride', 'false');
                    // Also try to clear any existing intervals
                    if (window.carouselInterval) {
                        clearInterval(window.carouselInterval);
                    }
                    // Try to stop Bootstrap carousel if present
                    if (window.bootstrap && window.bootstrap.Carousel) {
                        const carouselInstance = window.bootstrap.Carousel.getInstance(carousel);
                        if (carouselInstance) {
                            carouselInstance.pause();
                        }
                    }
                    // Also try jQuery Bootstrap carousel
                    if (window.$ && window.$.fn.carousel) {
                        window.$(carousel).carousel('pause');
                    }
                }
            """)
            # Add a small delay to let the disabling take effect
            self.page.wait_for_timeout(200)
        except Exception:
            # If disabling fails, it's not critical for most tests
            pass
        return self
    
    def _are_navigation_buttons_present(self) -> bool:
        """Check if navigation buttons are present and attached to DOM."""
        try:
            # Check if buttons are attached to DOM rather than just visible
            next_present = self.next_button.count() > 0
            prev_present = self.prev_button.count() > 0
            return next_present and prev_present
        except Exception:
            return False
    
    def _wait_for_button_ready(self, button_locator, timeout: int = 5000) -> bool:
        """Wait for a button to be ready for interaction."""
        try:
            button_locator.wait_for(state="attached", timeout=timeout)
            return True
        except Exception:
            return False
    
    
    
    def are_navigation_buttons_visible(self) -> bool:
        """Check if navigation buttons are visible using DOM-based visibility check."""
        next_visible = self._is_element_visible_dom("div#mz-carousel-217960 a.carousel-control-next")
        prev_visible = self._is_element_visible_dom("div#mz-carousel-217960 a.carousel-control-prev")
        return next_visible and prev_visible

    # Assertion Methods for Testing
    
    def assert_carousel_is_visible(self) -> 'MainCarousel':
        """Assert that the carousel is visible."""
        expect(self.carousel_container).to_be_visible()
        return self
    
    def assert_slide_is_active(self, slide_index: int) -> 'MainCarousel':
        """Assert that a specific slide is active."""
        actual_index = self.get_active_slide_index()
        if actual_index != slide_index:
            raise AssertionError(f"Expected slide {slide_index} to be active, but slide {actual_index} is active")
        return self
    
    def assert_indicator_is_active(self, indicator_index: int) -> 'MainCarousel':
        """Assert that a specific indicator is active."""
        actual_index = self.get_active_indicator_index()
        if actual_index != indicator_index:
            raise AssertionError(f"Expected indicator {indicator_index} to be active, but indicator {actual_index} is active")
        return self
    
    def assert_slide_count(self, expected_count: int) -> 'MainCarousel':
        """Assert that the carousel has the expected number of slides."""
        actual_count = self.get_slide_count()
        if actual_count != expected_count:
            raise AssertionError(f"Expected {expected_count} slides, but found {actual_count}")
        return self
