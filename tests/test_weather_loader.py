from etl.loaders.weather_loader import WeatherLoader

loader = WeatherLoader()

loader.load(
    "data/raw/nasa_power_historical.csv"
)