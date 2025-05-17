import logging
import os

from playwright.sync_api import Page

from pages.city_weather_page import CityWeatherPage
from pages.home_page import HomePage
from pages.weather_page import WeatherPage
from utils.helpers import get_weather_via_api, report_generator
from weather_db import WeatherDataBase

logger = logging.getLogger(__name__)


def test_weather_data(page: Page):
    """
    Test weather data collection and analysis.
    The test:
    1. Navigates to timeanddate.com
    2. Collects weather data for random cities
    3. Compares with OpenWeatherMap API data
    4. Generates a report of discrepancies
    """
    logger.info("Starting weather testing & analysis report")
    api_key = os.environ.get('API_KEY')
    threshold = int(os.environ.get('THRESHOLD'))

    weather_db = WeatherDataBase()
    weather_db.connect()
    weather_db.create_table()

    home = HomePage(page)
    logger.info("Navigating to timeanddate.com")
    home.goto_home()
    home.wait_page_load()
    home.navigate_to_weather()
    home.wait_page_load()
    weather_page = WeatherPage(home.page)

    logger.info("Getting all cities")
    table = weather_page.get_cities_table()
    cities = weather_page.get_cities(table)

    logger.info("Getting 20 random cities")
    cities_list = weather_page.get_random_cities(cities)
    cities_elements = weather_page.get_cities_elements(table, cities_list)
    cities_weather_dict = {}

    # get data via web and api for each city
    for city, element in cities_elements.items():
        logger.info(f"Getting weather data for {city}")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        api_temperature_celsius, api_feels_like_temp_celsius = get_weather_via_api(url)

        weather_page.click_on_city(element)
        city_page = CityWeatherPage(weather_page.page)
        cities_weather_dict[city] = city_page.get_city_weather(city)
        city_page.go_back()

        cities_weather_dict[city]['api_temp'] = api_temperature_celsius
        cities_weather_dict[city]['feels_like_api'] = api_feels_like_temp_celsius

    # Insert weather data to DB.
    for city, data in cities_weather_dict.items():
        weather_db.insert_weather_data(
            city, data["web_temp"], data["feels_like_web"], data["api_temp"], data["feels_like_api"])

    # get data from DB.
    cities_with_large_diff = weather_db.get_cities_where_diff_larger_than_threshold(threshold=threshold)
    mean, max_val, min_val = weather_db.get_summary_statistics()

    report_generator(cities_with_large_diff, mean, max_val, min_val)
    weather_db.close()
