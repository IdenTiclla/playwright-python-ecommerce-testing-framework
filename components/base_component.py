from playwright.sync_api import Page

class BaseComponent:
    def __init__(self, page: Page):
        self.page = page

    
    def _is_element_visible_dom(self, selector: str) -> bool:
        """Check element visibility using DOM properties instead of Playwright's is_visible()."""
        try:
            return self.page.evaluate(f"""
                () => {{
                    const element = document.querySelector('{selector}');
                    return element ? (element.offsetWidth > 0 && element.offsetHeight > 0) : false;
                }}
            """)
        except Exception:
            return False
        
    def is_element_not_visible_dom(self, selector: str) -> bool:
        """Check if the element is not visible using DOM properties instead of Playwright's is_visible()."""
        return not self._is_element_visible_dom(selector)
    
    def is_element_enabled(self, selector: str) -> bool:
        """Check if the element is enabled."""
        return self.page.evaluate(f"""
            () => {{
                const element = document.querySelector('{selector}');
                if (!element) return false;
                return !element.disabled && element.hasAttribute('aria-disabled');
            }}
        """)
    
    def is_element_disabled(self, selector: str) -> bool:
        """Check if the element is disabled."""
        return not self.is_element_enabled(selector)    
    