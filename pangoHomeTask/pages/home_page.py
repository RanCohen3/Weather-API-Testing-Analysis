import logging

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    URL = "https://www.timeanddate.com/"
    NAV_TITLE = 'a.site-nav__title'

    def __init__(self, page):
        super().__init__(page)

    def goto_home(self):
        """
        This method navigates to home page
        """
        self.open_page(self.URL)

    def navigate_to_weather(self):
        """
        This method navigates to the weather page
        """
        self.page.locator(self.NAV_TITLE, has_text='Weather').click()
