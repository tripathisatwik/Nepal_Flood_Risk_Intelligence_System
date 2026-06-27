from etl.loaders.elevation_loader import ElevationLoader

loader = ElevationLoader()

loader.load(
    "data/raw/district_elevation.csv"
)