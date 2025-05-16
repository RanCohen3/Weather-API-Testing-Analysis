import math

import pandas as pd


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

    with open("weather_info.csv", "w", encoding="utf-8") as f:
        data_df.to_csv(f, index=False)
        f.write("\n\nSummary statistics\n")
        summary_stats_df.to_csv(f, index=False)
