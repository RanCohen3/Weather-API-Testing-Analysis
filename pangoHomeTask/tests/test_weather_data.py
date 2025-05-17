import logging
import os

from utils.helpers import report_generator, get_weather_via_api
from pages.city_weather_page import CityWeatherPage
from pages.weather_page import WeatherPage
from pages.home_page import HomePage
from weather_db import WeatherDataBase

logger = logging.getLogger(__name__)


def test_weather_data(page):
    logger.info("Starting weather testing & analysis report")
    api_key = os.environ.get("API_KEY")
    threshold = int(os.environ.get("THRESHOLD"))

    # scraping data
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

    for city, element in cities_elements.items():
        logger.info(f"Getting weather data for {city}")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        # response = requests.get(url)
        # response.raise_for_status()
        # main_data = response.json()["main"]
        # api_temperature = main_data["temp"]
        # api_feels_like_temp = main_data["feels_like"]
        #
        # api_temperature_celsius = kelvin_to_celsius(api_temperature)
        # api_feels_like_temp_celsius = kelvin_to_celsius(api_feels_like_temp)

        api_temperature_celsius, api_feels_like_temp_celsius = get_weather_via_api(url)

        weather_page.click_on_city(element)
        city_page = CityWeatherPage(weather_page.page)
        cities_weather_dict[city] = city_page.get_city_weather(city)
        city_page.go_back()

        cities_weather_dict[city]['api_temp'] = api_temperature_celsius
        cities_weather_dict[city]['feels_like_api'] = api_feels_like_temp_celsius

    weather_db = WeatherDataBase()
    weather_db.connect()

    # create table
    weather_db.create_table()
    for city, data in cities_weather_dict.items():
        weather_db.insert_weather_data(
            city, data["web_temp"], data["feels_like_web"], data["api_temp"], data["feels_like_api"])

    cities_with_large_diff = weather_db.get_cities_where_diff_larger_than_threshold(threshold=threshold)
    mean, max_val, min_val = weather_db.get_summary_statistics()

    weather_db.close()

    report_generator(cities_with_large_diff, mean, max_val, min_val)
