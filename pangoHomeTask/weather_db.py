import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


class WeatherDataBase:
    def __init__(self):
        self.conn = None

    def connect(self):
        """
        Connect to the DB.
        """
        try:
            logger.info("Trying to connect to DB")
            os.makedirs("db", exist_ok=True)
            self.conn = sqlite3.connect("db/weather_data.db")
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")

    def close(self):
        """
        Closing the connection to the DB.
        """
        logger.info("Closing the connection to the DB")
        self.conn.close()

    def create_table(self):
        """
        Create a table for the DB in case it does not exist.
        :return:
        """
        logger.info("Creating a table")
        self.reset_weather_table()

        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                city TEXT,
                temperature_web REAL,
                feels_like_web REAL,
                temperature_api REAL,
                feels_like_api REAL,
                avg_temperature REAL GENERATED ALWAYS AS ((temperature_web + temperature_api) / 2) STORED,
                diff_temperature REAL GENERATED ALWAYS AS (ABS(temperature_web - temperature_api)) STORED
            )
        """)

        res = cursor.execute("SELECT name FROM sqlite_master")
        if not res.fetchone():
            raise sqlite3.Error("Could not create the table")

    def insert_weather_data(self, city_name, temperature_web, feels_like_web,
                            temperature_api, feels_like_api):
        """
        Insert weather data for a city.
        :param city_name: Name of the city
        :param temperature_web: Temperature from web scraping
        :param feels_like_web: "Feels like" temperature from web scraping
        :param temperature_api: Temperature from API
        :param feels_like_api: "Feels like" temperature from API
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO weather_data (
                city,
                temperature_web,
                feels_like_web,
                temperature_api,
                feels_like_api
            ) VALUES (?, ?, ?, ?, ?)
        """, (city_name, temperature_web, feels_like_web, temperature_api, feels_like_api))

        self.conn.commit()

    def get_cities_where_diff_larger_than_threshold(self, threshold):
        """
        Get all cities where the difference larger than threshold
        :param threshold:
        """
        logger.info(f"Getting cities where threshold is larger than {threshold}")
        cursor = self.conn.cursor()
        query = '''
            SELECT 
                city,
                temperature_web,
                feels_like_web,
                temperature_api,
                feels_like_api,
                avg_temperature,
                diff_temperature
            FROM weather_data
            WHERE diff_temperature >= ?
        '''

        cursor.execute(query, (threshold,))
        cities_with_large_diff = cursor.fetchall()

        return cities_with_large_diff

    def get_summary_statistics(self):
        """
        Calculate and return summary statistics for the temperature differences stored in the DB.
        """
        logger.info("Getting summary statistics")
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                AVG(diff_temperature),
                MAX(diff_temperature),
                MIN(diff_temperature)
            FROM weather_data
        """)
        mean, max_val, min_val = cursor.fetchone()

        return mean, max_val, min_val

    def reset_weather_table(self):
        """
        In case the DB table already exists, it deletes it so data won't be duplicated.
        :return:
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name='weather_data'
        """)
        if cursor.fetchone():
            cursor.execute("DELETE FROM weather_data")
            self.conn.commit()
