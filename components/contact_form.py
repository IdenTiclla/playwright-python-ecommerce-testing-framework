from playwright.sync_api import Page
from components.base_component import BaseComponent

class ContactForm(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.container = page.locator("div.modal-dialog-centered.modal-md")
        self.close_button = page.locator("div.modal-dialog-centered.modal-md button[type='button'][class*='close']")
        self.name_input = page.locator("div.modal-dialog-centered.modal-md input[name='name']")
        self.email_input = page.locator("div.modal-dialog-centered.modal-md input[name='email']")
        self.subject_input = page.locator("div.modal-dialog-centered.modal-md input[name='subject']")
        self.message_input = page.locator("div.modal-dialog-centered.modal-md textarea[name='message']")
        self.submit_button = page.locator("div.modal-dialog-centered.modal-md button[type='submit']")

    def fill_contact_form(self, name: str, email: str, subject: str, message: str):
        """Fill the contact form"""

        self.name_input.clear()
        self.name_input.fill(name)

        self.email_input.clear()
        self.email_input.fill(email)
        
        self.subject_input.clear()
        self.subject_input.fill(subject)
        
        self.message_input.clear()
        self.message_input.fill(message)
        
        self.submit_button.click()

    def is_contact_form_visible(self):
        """Check if the contact form is visible"""
        return self.container.is_visible()

    def close(self):
        """Close the contact form"""
        self.close_button.click()