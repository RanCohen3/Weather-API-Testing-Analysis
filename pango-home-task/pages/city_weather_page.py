import logging
import re

from .base_page import BasePage
from playwright.sync_api import Page

logger = logging.getLogger(__name__)


class CityWeatherPage(BasePage):
    """
    Page object for individual city weather pages on timeanddate.com.
    """
    def __init__(self, page: Page):
        """
        Initialize the CityWeatherPage with a Playwright page object.
        :param page: Playwright page object.
        """
        super().__init__(page)

    def get_city_weather(self, city):
        """
        Extract weather data for a specific city from the page.
        :param city: Name of the city for logging purposes
        """
        def extract_feels_like_number(p_element_with_feels_like):
            """
            Extract the 'Feels Like' temperature.
            :param p_element_with_feels_like: Locator for the paragraph element containing
            'Feels Like' text
            """
            raw_text = p_element_with_feels_like.text_content()
            match = re.search(r'Feels Like:\s*(\d+)', raw_text)
            if match:
                feel_temp = int(match.group(1))
            else:
                feel_temp = None
            return feel_temp

        def extract_now_temperature(container):
            """
            Extract the current temperature from the weather container.
            :param container: Locator for the temperature container element
            """
            raw_text = container.locator('div.h2').text_content()

            match = re.search(r'-?\d+', raw_text)
            if match:
                temp = int(match.group())
            else:
                temp = None
            return temp

        logger.info(f'Extracting {city} weather from web')
        city_dict = {}
        container = self.page.locator('#qlook')
        city_dict['web_temp'] = extract_now_temperature(container)

        p_element_with_feels_like = self.page.locator('p', has_text='Feels Like')
        city_dict['feels_like_web'] = extract_feels_like_number(p_element_with_feels_like)

        return city_dict

