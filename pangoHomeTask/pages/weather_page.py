import random

from .base_page import BasePage
from playwright.sync_api import Page


class WeatherPage(BasePage):
    """
    Page object for the Airbnb listing details page
    """
    def __init__(self, page: Page):
        super().__init__(page)

    def get_cities_table(self):
        """
        This method returns the table object of the cities
        :return:
        """
        return self.page.get_by_role("table")

    def get_cities(self, table):
        """
        This method return the cities objects
        :param table: Table object from weather page
        """
        return table.locator("a")

    def get_random_cities(self, cities):
        """
        This method gets 20 random cities.
        :param cities:
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
        # TODO should be 20
        # return random.sample(list(filtered_city_dict.items()), 20)
        return random.sample(list(filtered_city_dict.items()), 5)

    def get_cities_elements(self, table, city_index_pairs):
        """
        This method goes over the random 20 city:index pairs, and returns the city with its locator.
        :param table: Table element from weather page
        :param city_index_pairs: random 20 pairs of city:index
        """
        city_locator_dict = {}
        for city, index in city_index_pairs:
            city_locator_dict[city] = table.locator("a").nth(index)

        return city_locator_dict

    def click_on_city(self, city_locator):
        """
        Click on city
        :param city_locator: locator
        """
        city_locator.click()
