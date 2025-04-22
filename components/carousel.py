from playwright.sync_api import Page

class Carousel:
    def __init__(self, page: Page):
        self.page = page
        # Selector for the carousel displaying smart watch, camera, and iPhone
        self.carousel_selector = "div#mz-carousel-217960"
        self.slide_selector = f"{self.carousel_selector} .carousel-item"
        self.next_button_selector = f"{self.carousel_selector} a.carousel-control-next"
        self.prev_button_selector = f"{self.carousel_selector} a.carousel-control-prev"
        self.active_slide_selector = f"{self.carousel_selector} .carousel-item.active"

    def is_visible(self):
        return self.page.locator(self.carousel_selector).is_visible()

    def get_slide_count(self):
        return self.page.locator(self.slide_selector).count()

    def go_to_next_slide(self):
        self.page.click(self.next_button_selector, force=True)

    def go_to_prev_slide(self):
        self.page.click(self.prev_button_selector, force=True)

    def get_active_slide_index(self):
        slides = self.page.locator(self.slide_selector)
        for i in range(slides.count()):
            if 'active' in (slides.nth(i).get_attribute('class') or ''):
                return i
        return -1
