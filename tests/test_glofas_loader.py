from etl.loaders.glofas_loader import GlofasLoader

loader = GlofasLoader()

loader.load(
    "data/raw/glofas_discharge.csv"
)