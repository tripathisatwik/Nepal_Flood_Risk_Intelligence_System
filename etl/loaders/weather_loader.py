import pandas as pd

from sqlalchemy import text

from database.db_connection import DatabaseConnection
from etl.utils.district_mapper import DistrictMapper


class WeatherLoader:

    def __init__(self):
        self.engine = DatabaseConnection().get_engine()
        self.mapper = DistrictMapper()

    def load(self, csv_path, chunk_size=5000):

        total_rows = 0

        for chunk in pd.read_csv(
            csv_path,
            chunksize=chunk_size
        ):

            chunk["date"] = pd.to_datetime(
                chunk["date"],
                format="%d/%m/%Y"
            )

            chunk["district_id"] = chunk["district"].apply(
                self.mapper.get_district_id
            )

            chunk = chunk.dropna(
                subset=["district_id"]
            )

            weather_df = pd.DataFrame({
                "district_id": chunk["district_id"].astype(int),
                "record_date": chunk["date"],
                "rainfall_mm": chunk["rainfall_mm"],
                "temp_max_c": chunk["temp_max_c"],
                "temp_min_c": chunk["temp_min_c"],
                "humidity_pct": chunk["humidity_pct"],
                "wind_ms": chunk["wind_ms"]
            })

            weather_df.to_sql(
                "weather_daily",
                self.engine,
                if_exists="append",
                index=False,
                method="multi"
            )

            total_rows += len(weather_df)

            print(
                f"Loaded {total_rows:,} weather rows..."
            )

        print(
            f"\nFinished loading {total_rows:,} rows."
        )