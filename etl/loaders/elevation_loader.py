import pandas as pd

from database.db_connection import DatabaseConnection
from etl.utils.district_mapper import DistrictMapper


class ElevationLoader:

    def __init__(self):
        self.engine = DatabaseConnection().get_engine()
        self.mapper = DistrictMapper()

    def load(self, csv_path):

        df = pd.read_csv(csv_path)

        conn = self.engine.raw_connection()
        cursor = conn.cursor()

        updated = 0

        for _, row in df.iterrows():

            district_id = self.mapper.get_district_id(
                row["district"]
            )

            if district_id is None:
                continue

            cursor.execute(
                """
                UPDATE districts
                SET
                    latitude = %s,
                    longitude = %s,
                    elevation_m = %s
                WHERE district_id = %s
                """,
                (
                    float(row["latitude"]),
                    float(row["longitude"]),
                    float(row["elevation_m"]),
                    district_id
                )
            )

            updated += 1

        conn.commit()

        cursor.close()
        conn.close()

        print(
            f"Updated {updated} districts."
        )