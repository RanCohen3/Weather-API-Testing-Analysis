# Weather API Testing & Analysis Project

This project compares real-time temperature readings from timeanddate.com and OpenWeatherMap API for 20 random cities,
storing and analyzing the data to generate CSV report.

## Prerequisites

- OpenWeatherMap API key (get one at [OpenWeatherMap](https://openweathermap.org/api))


## Installation

1. Clone the repository:
```bash
git clone git@github.com:RanCohen3/weather-api-testing-analysis.git
cd weather-api-testing-analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install
```

## Configuration

1. Obtain an API key from OpenWeatherMap:
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api)
   - Copy your API key

2. (Optional) Configure the temperature threshold:
   - The default threshold is 2 degrees Celsius

## Usage

### Running the Analysis

Run the main script with your OpenWeatherMap API key:

```bash
python main.py --api_key YOUR_API_KEY_HERE --threshold 2
```

Parameters:
- `--api_key`: (Required) Your OpenWeatherMap API key
- `--threshold`: (Optional) Temperature difference threshold in Celsius (default: 2)


## Output

The script generates a CSV report containing:
- Temperature readings from both sources
- Average temperatures
- Discrepancy analysis
- Summary statistics (mean, max, min discrepancy)
