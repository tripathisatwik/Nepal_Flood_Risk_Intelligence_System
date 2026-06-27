from etl.loaders.flood_incidents_loader import (
    FloodIncidentsLoader
)

loader = FloodIncidentsLoader()

loader.load(
    "data/raw/flood_incidents.xlsx"
)