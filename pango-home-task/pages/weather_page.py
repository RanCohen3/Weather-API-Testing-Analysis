import random

from .base_page import BasePage
from playwright.sync_api import Page


class WeatherPage(BasePage):
    """
    Page object for the timeanddate.com weather page.
    """
    
    def __init__(self, page: Page):
        """
        Initialize the WeatherPage.
        :param page: Playwright page object.
        """
        super().__init__(page)

    def get_cities_table(self):
        """
        Get the table element containing city information.
        """
        return self.page.get_by_role('table')

    def get_cities(self, table):
        """
        Get all city elements from the table.
        :param table: Locator for the cities table
        """
        return table.locator('a')

    def get_random_cities(self, cities):
        """
        Select random cities from the available list.
        Filters out cities that are not available in the OpenWeatherMap API
        and returns a random selection of cities for weather comparison.
        :param cities: Locator containing all city elements
        """
        cities_texts = enumerate(cities.all_inner_texts())

        city_dict = {}
        filtered_city_dict = {}

        for index, city in cities_texts:
            city_dict[city] = index

        # list of excluded cities that does not exist via api
        excluded_cities = ['Kiritimati']
        for city, index in city_dict.items():
            if city not in excluded_cities:
                filtered_city_dict[city] = index

        return random.sample(list(filtered_city_dict.items()), 20)

    def get_cities_elements(self, table, city_index_pairs):
        """
        Get Playwright locators for selected cities.
        :param table: Locator for the cities table
        :param city_index_pairs: List of (city_name, index) tuples
        """
        city_locator_dict = {}
        for city, index in city_index_pairs:
            city_locator_dict[city] = table.locator('a').nth(index)

        return city_locator_dict

    def click_on_city(self, city_locator):
        """
        Navigate to a specific city's weather page.
        :param city_locator: Locator for the city element
        """
        city_locator.click()
