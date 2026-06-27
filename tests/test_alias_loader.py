from etl.loaders.alias_loader import AliasLoader

loader = AliasLoader()

loader.load(
    "data/reference/district_aliases.csv"
)
