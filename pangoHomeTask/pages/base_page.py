import logging
from playwright.sync_api import Page

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open_page(self, url):
        """
        This method navigates to the URL
        :param url: URL address
        """
        self.page.goto(url, timeout=1000 * 60)

    def wait_page_load(self):
        logging.info("Waiting for the page to load")
        self.page.wait_for_load_state('domcontentloaded')
        # Sometimes JS takes time to execute, adding 5 sec delay
        self.page.wait_for_timeout(1000 * 5)

    def go_back(self):
        """
        Navigate to the previous web page
        """
        self.page.go_back()
