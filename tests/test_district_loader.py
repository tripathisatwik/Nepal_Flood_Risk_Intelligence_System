from etl.loaders.district_loader import DistrictLoader

loader = DistrictLoader()

loader.load(
    "data/raw/district_elevation.csv"
)