import pandas as pd

from sqlalchemy import text

from database.db_connection import DatabaseConnection
from etl.utils.district_mapper import DistrictMapper


class AliasLoader:

    def __init__(self):
        self.engine = DatabaseConnection().get_engine()

    def load(self, csv_path):

        mapper = DistrictMapper()

        df = pd.read_csv(csv_path)

        inserted = 0

        with self.engine.begin() as connection:

            for _, row in df.iterrows():

                district_id = mapper.get_district_id(
                    row["district_name"]
                )

                if district_id is None:
                    continue

                connection.execute(
                    text("""
                        INSERT INTO district_aliases
                        (
                            alias_name,
                            district_id
                        )
                        VALUES
                        (
                            :alias_name,
                            :district_id
                        )
                        ON CONFLICT (alias_name)
                        DO NOTHING
                    """),
                    {
                        "alias_name": row["alias_name"],
                        "district_id": district_id
                    }
                )

                inserted += 1

        print(f"{inserted} aliases processed.")