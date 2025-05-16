import re

from .base_page import BasePage
from playwright.sync_api import Page
import logging


class CityWeatherPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.logger = logging.getLogger(__name__)

    def get_city_weather(self, city):
        def extract_feels_like_number(p_element_with_feels_like):
            """
            Extracts the 'Feels Like' temperature number from a <p> element.
            """
            raw_text = p_element_with_feels_like.text_content()
            match = re.search(r"Feels Like:\s*(\d+)", raw_text)
            if match:
                feel_temp = int(match.group(1))
            else:
                feel_temp = None
            return feel_temp

        def extract_now_temperature(container):
            """
            This inner method extract the now temperature
            :param container: The container contains the data
            """
            raw_text = container.locator("div.h2").text_content()

            match = re.search(r"-?\d+", raw_text)
            if match:
                temp = int(match.group())
            else:
                temp = None
            return temp

        logging.info(f"Extracting {city}'s weather from web")
        city_dict = {}
        container = self.page.locator("#qlook")
        city_dict["web_temp"] = extract_now_temperature(container)

        p_element_with_feels_like = self.page.locator("p", has_text="Feels Like")
        city_dict["feels_like_web"] = extract_feels_like_number(p_element_with_feels_like)

        return city_dict

