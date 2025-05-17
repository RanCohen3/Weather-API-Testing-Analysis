import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


class WeatherDataBase:
    """
    A class to manage SQLite database operations for weather data.
    """
    def __init__(self):
        """
        Initialize the WeatherDataBase instance.
        """
        self.conn = None

    def connect(self):
        """
        Establish a connection to the SQLite database
        Creates a 'db' directory if it doesn't exist and connects to 'weather_data.db'.
        """
        try:
            logger.info('Trying to connect to DB')
            os.makedirs('db', exist_ok=True)
            self.conn = sqlite3.connect('db/weather_data.db')
        except sqlite3.Error as e:
            logger.error(f'Database connection error: {e}')

    def close(self):
        """
        Close the database connection.
        """
        if self.conn is not None:
            logger.info('Closing the connection to the DB')
            self.conn.close()

    def create_table(self):
        """
        Create the weather_data table if it doesn't exist.
        Creates a table with the following columns:
        
        - city: City name
        - temperature_web: Temperature from web scraping
        - feels_like_web: "Feels like" temperature from web scraping
        - temperature_api: Temperature from API
        - feels_like_api: "Feels like" temperature from API
        - avg_temperature: Computed average of web and API temperatures
        - diff_temperature: Computed absolute difference between web and API temperatures
        """
        logger.info('Creating a table')
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
            raise sqlite3.Error('Could not create the table')

    def get_cities_where_diff_larger_than_threshold(self, threshold):
        """
        Retrieve cities where temperature difference exceeds the threshold.
        :param threshold: Temperature difference threshold in Celsius
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
            WHERE diff_temperature > ?
        '''

        cursor.execute(query, (threshold,))
        cities_with_large_diff = cursor.fetchall()

        return cities_with_large_diff

    def insert_weather_data(self, city_name, temperature_web, feels_like_web, temperature_api,
                            feels_like_api):
        """
        Insert weather data for a city into the database.

        :param city_name: Name of the city
        :param temperature_web: Temperature from web scraping in Celsius
        :param feels_like_web: "Feels like" temperature from web scraping in Celsius
        :param temperature_api: Temperature from API in Celsius
        :param feels_like_api: "Feels like" temperature from API in Celsius
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

    def get_summary_statistics(self):
        """
        Calculate summary statistics for temperature differences.
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
        Reset the weather_data table by deleting all existing records.
        This method is called before creating a new table to ensure no duplicate
        data exists.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name='weather_data'
        """)
        if cursor.fetchone():
            cursor.execute("DELETE FROM weather_data")
            self.conn.commit()
