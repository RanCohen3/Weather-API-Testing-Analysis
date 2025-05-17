import logging

from pages.base_page import BasePage
from playwright.sync_api import Page

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """
    Page object for the timeanddate.com home page.
    """

    URL = "https://www.timeanddate.com/"
    NAV_TITLE = 'a.site-nav__title'

    def __init__(self, page: Page):
        """
        Initialize the HomePage.
        :param page: Playwright page object.
        """
        super().__init__(page)

    def goto_home(self):
        """
        Navigate to timeanddate.com home page.
        """
        self.open_page(self.URL)

    def navigate_to_weather(self):
        """
        Navigate to the weather section of the website.
        """
        self.page.locator(self.NAV_TITLE, has_text='Weather').click()
