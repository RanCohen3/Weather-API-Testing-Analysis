import math
import os

import pandas as pd
import requests


def kelvin_to_celsius(kelvin):
    """
    This converts Kelvin degrees to Celsius .
    :param kelvin: Temperature in Kelvin.
    """
    return math.ceil(kelvin - 273.15)


def report_generator(cities_with_large_diff, mean, max_val, min_val):
    """
    This function generates the CSV file report with the weather data.
    :param cities_with_large_diff: Cities
    :param mean: Mean value of different
    :param max_val: Max value of different
    :param min_val: Min value of different
    """
    cities_data_dict = {
        "cities": [row[0] for row in cities_with_large_diff],
        "web_temp": [row[1] for row in cities_with_large_diff],
        "web_feels_like": [row[2] for row in cities_with_large_diff],
        "api_temp": [row[3] for row in cities_with_large_diff],
        "api_feels_like": [row[4] for row in cities_with_large_diff],
        "avg_temperature": [row[5] for row in cities_with_large_diff],
        "diff_temperature": [row[6] for row in cities_with_large_diff]
    }

    summary_dict = {
        "mean_discrepancy": mean,
        "max_discrepancy": max_val,
        "min_discrepancy": min_val
    }

    data_df = pd.DataFrame(cities_data_dict)
    summary_stats_df = pd.DataFrame([summary_dict])

    os.makedirs("reports", exist_ok=True)
    with open("reports/weather_info.csv", "w", encoding="utf-8") as f:
        data_df.to_csv(f, index=False)
        f.write("\n\nSummary statistics\n")
        summary_stats_df.to_csv(f, index=False)


def get_weather_via_api(url):
    """
    This function GET weather data via API request.
    :param url: URL.
    """
    response = requests.get(url)
    response.raise_for_status()
    main_data = response.json()["main"]
    api_temperature = main_data["temp"]
    api_feels_like_temp = main_data["feels_like"]

    api_temperature_celsius = kelvin_to_celsius(api_temperature)
    api_feels_like_temp_celsius = kelvin_to_celsius(api_feels_like_temp)

    return api_temperature_celsius, api_feels_like_temp_celsius
