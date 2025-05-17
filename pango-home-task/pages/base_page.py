import logging
from playwright.sync_api import Page

logger = logging.getLogger(__name__)


class BasePage:
    """
    Base class for all page objects in the application.
    """
    def __init__(self, page: Page):
        """
        Initialize the BasePage with a Playwright page object.
        :param page: Playwright page object.
        """
        self.page: Page = page

    def open_page(self, url):
        """
        Navigate to a specific URL.
        :param url: The URL to navigate to
        """
        self.page.goto(url, timeout=1000 * 60)

    def wait_page_load(self):
        """
        Wait for the page to fully load.
        """
        logging.info('Waiting for the page to load')
        self.page.wait_for_load_state('domcontentloaded')
        # Sometimes JS takes time to execute, adding 5 sec delay
        self.page.wait_for_timeout(1000 * 5)

    def go_back(self):
        """
        Navigate to the previous page in browser history.
        """
        self.page.go_back()
