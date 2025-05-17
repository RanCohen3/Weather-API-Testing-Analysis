import argparse
import os

import pytest


def main():
    parser = argparse.ArgumentParser(description="Run weather data tests with parameters.")
    parser.add_argument("--threshold", default=2, help="Threshold for temperature diff")
    parser.add_argument("--api_key", required=True, help="API key for weather data")

    args = parser.parse_args()

    os.environ["THRESHOLD"] = str(args.threshold)
    os.environ["API_KEY"] = args.api_key

    tests = ["tests/test_weather_data.py"]
    pytest.main(tests)


if __name__ == '__main__':
    main()

