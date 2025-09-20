from playwright.sync_api import Page
from components.base_component import BaseComponent
from components.alert import Alert

class CommentForm(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.your_name_input = page.locator("input[name='name']")
        self.email_input = page.locator("input[name='email']")
        self.comment_input = page.locator("textarea#input-comment")
        self.post_comment_button = page.locator("button#button-comment")

        # Alert
        self.alert = Alert(page)

    def post_comment(self):
        self.post_comment_button.click()

    def submit_comment(self, name: str, email: str, comment: str):
        self.your_name_input.clear()
        self.your_name_input.fill(name)
        self.email_input.clear()
        self.email_input.fill(email)
        self.comment_input.clear()
        self.comment_input.fill(comment)
        self.post_comment()

    def get_your_name_class(self):
        return self.your_name_input.get_attribute("class")

    def get_email_input_class(self):
        return self.email_input.get_attribute("class")
    
    def get_comment_input_class(self):
        return self.comment_input.get_attribute("class")

    
