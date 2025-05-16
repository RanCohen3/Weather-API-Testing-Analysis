import argparse
import os

import pytest


def main():
    api_key: str = os.environ.get("API_KEY")
    if not api_key:
        print("missing API key env var")
        return

    threshold: str = os.environ.get("THRESHOLD")
    if not threshold:
        print("missing threshold env var")
        return
    # same for other key

    tests = ["tests/test_weather_data.py"]
    pytest.main(tests)


if __name__ == '__main__':
    main()

