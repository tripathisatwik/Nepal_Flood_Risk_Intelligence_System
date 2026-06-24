import pandas as pd

from sqlalchemy import text

from database.db_connection import DatabaseConnection


class DistrictLoader:

    def __init__(self):
        self.engine = DatabaseConnection().get_engine()

    def load(self, csv_path):

        df = pd.read_csv(csv_path)

        records_inserted = 0

        with self.engine.begin() as connection:

            for _, row in df.iterrows():

                query = text("""
                    INSERT INTO districts
                    (
                        district_name,
                        latitude,
                        longitude,
                        elevation_m
                    )
                    VALUES
                    (
                        :district_name,
                        :latitude,
                        :longitude,
                        :elevation_m
                    )
                    ON CONFLICT (district_name)
                    DO NOTHING
                """)

                connection.execute(
                    query,
                    {
                        "district_name": row["district"],
                        "latitude": row["latitude"],
                        "longitude": row["longitude"],
                        "elevation_m": row["elevation_m"]
                    }
                )

                records_inserted += 1

        print(f"{records_inserted} district records processed.")