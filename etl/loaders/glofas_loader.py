import pandas as pd

from database.db_connection import DatabaseConnection
from etl.utils.district_mapper import DistrictMapper


class GlofasLoader:

    def __init__(self):
        self.engine = DatabaseConnection().get_engine()
        self.mapper = DistrictMapper()

    def load(self, csv_path):

        print("Loading GloFAS discharge data...")

        df = pd.read_csv(csv_path)

        conn = self.engine.raw_connection()
        cursor = conn.cursor()

        inserted = 0
        skipped = 0

        for _, row in df.iterrows():

            district_id = self.mapper.get_district_id(
                str(row["district"]).strip()
            )

            if district_id is None:
                skipped += 1
                continue

            record_date = pd.to_datetime(
                row["date"],
                dayfirst=True,
                errors="coerce"
            )

            if pd.isna(record_date):
                skipped += 1
                continue

            cursor.execute(
                """
                INSERT INTO river_discharge_daily ( 
                    district_id,
                    record_date,
                    discharge_m3s
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (
                    district_id,
                    record_date
                )
                DO NOTHING
                """,
                (
                    district_id,
                    record_date.date(),
                    float(row["discharge_m3s"])
                )
            )

            inserted += 1

            if inserted % 50000 == 0:
                print(f"Processed {inserted:,} rows...")

        conn.commit()

        cursor.close()
        conn.close()

        print(f"Inserted : {inserted}")
        print(f"Skipped  : {skipped}")