from playwright.sync_api import Page
from components.base_component import BaseComponent

class ReviewForm(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.name_input = page.locator("form.form-horizontal input#input-name")
        self.review_input = page.locator("form.form-horizontal textarea#input-review")
        self.submit_button = page.locator("form.form-horizontal button#button-review")

        self.error_message = page.locator("form.form-horizontal div.alert")


    def fill_name(self, name: str):
        self.name_input.fill(name)

    def fill_review(self, review: str):
        self.review_input.fill(review)

    def submit(self):
        self.submit_button.click()

    def select_rating(self, rating: int):
        rating_start = self.page.locator(f"label[for='rating-{rating}-216860']")
        rating_start.click()

    def submit_review(self, rating:int, name:str, review:str):
        self.select_rating(rating)
        self.fill_name(name)
        self.fill_review(review)
        self.submit()

    def get_error_message(self):
        return self.error_message.inner_text().strip()