import pandas as pd

from database.db_connection import DatabaseConnection
from etl.utils.district_mapper import DistrictMapper


class RainfallIncidentsLoader:

    def __init__(self):
        self.engine = DatabaseConnection().get_engine()
        self.mapper = DistrictMapper()

    def load(self, excel_path):

        print("Loading Heavy Rainfall incidents...")

        df = pd.read_excel(excel_path)

        conn = self.engine.raw_connection()
        cursor = conn.cursor()

        inserted = 0
        skipped = 0

        for _, row in df.iterrows():

            district_name = str(row["District"]).strip()

            district_id = self.mapper.get_district_id(
                district_name
            )

            if district_id is None:
                skipped += 1
                continue

            incident_date = pd.to_datetime(
                row["Incident on"],
                dayfirst=True,
                errors="coerce"
            )

            if pd.isna(incident_date):
                skipped += 1
                continue

            def safe_int(value):
                if pd.isna(value):
                    return 0
                return int(value)

            cursor.execute(
                """
                INSERT INTO heavy_rain_incidents (
                    district_id,
                    municipality,
                    incident_date,
                    house_destroyed,
                    house_affected,
                    people_death,
                    people_injured,
                    people_missing,
                    agriculture_loss_npr,
                    infrastructure_loss_npr,
                    source
                )
                VALUES (
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                )
                """,
                (
                    district_id,
                    str(row.get("Municipality", "")),
                    incident_date.date(),

                    safe_int(row.get("House destroyed")),
                    safe_int(row.get("House affected")),

                    safe_int(row.get("Total - People Death")),
                    safe_int(row.get("Total - People Injured")),
                    safe_int(row.get("Total - People Missing")),

                    safe_int(
                        row.get(
                            "Agriculture economic loss (NPR)"
                        )
                    ),

                    safe_int(
                        row.get(
                            "Infrastructure economic loss (NPR)"
                        )
                    ),

                    str(row.get("Source", ""))
                )
            )

            inserted += 1

        conn.commit()

        cursor.close()
        conn.close()

        print(f"Inserted : {inserted}")
        print(f"Skipped  : {skipped}")