from etl.loaders.rainfall_incidents_loader import (
    RainfallIncidentsLoader
)

loader = RainfallIncidentsLoader()

loader.load(
    "data/raw/heavyrainfall_incidents.xlsx"
)