import os

import requests

from utils.helpers import report_generator, kelvin_to_celsius
from pages.city_weather_page import CityWeatherPage
from pages.weather_page import WeatherPage
from pages.home_page import HomePage
from weather_db import WeatherDataBase


def test_weather_data(page, *args, **kwargs):
    api_key = os.environ.get("API_KEY")
    threshold = int(os.environ.get("THRESHOLD"))
    print(f"threshold is {threshold}")
    print(f"my api is {api_key}")
    # api_key = "859b919dbc2542166e6a9ed88f7c72a8"

    # scraping data
    home = HomePage(page)
    home.goto_home()
    home.wait_page_load()
    home.navigate_to_weather()
    home.wait_page_load()
    weather_page = WeatherPage(home.page)
    table = weather_page.get_cities_table()
    cities = weather_page.get_cities(table)

    cities_list = weather_page.get_random_cities(cities)
    cities_elements = weather_page.get_cities_elements(table, cities_list)
    cities_weather_dict = {}

    for city, element in cities_elements.items():
        # TODO move all api to outside helper? new class?
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        main_data = response.json()["main"]
        api_temperature = main_data["temp"]
        api_feels_like_temp = main_data["feels_like"]

        api_temperature_celsius = kelvin_to_celsius(api_temperature)
        api_feels_like_temp_celsius = kelvin_to_celsius(api_feels_like_temp)

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
    # TODO switch threshold=3
    cities_with_large_diff = weather_db.get_cities_where_diff_larger_than_threshold(threshold=3)
    mean, max_val, min_val = weather_db.get_summary_statistics()

    weather_db.close()

    report_generator(cities_with_large_diff, mean, max_val, min_val)
