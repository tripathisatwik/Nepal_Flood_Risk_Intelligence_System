import pandas as pd
import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "flood_risk",
    "user": "postgres",
    "password": "postgres"
}


def safe_int(value):
    if pd.isna(value):
        return 0

    try:
        return int(value)
    except:
        return 0


def safe_float(value):
    if pd.isna(value):
        return 0.0

    try:
        return float(value)
    except:
        return 0.0


def main():

    print("Loading heavy rainfall incidents...")

    df = pd.read_csv(
        "data/raw/heavy_rainfall_incidents.csv"
    )

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    inserted = 0
    skipped = 0

    for _, row in df.iterrows():

        district = str(row["District"]).strip()

        cur.execute(
            """
            SELECT district_id
            FROM districts
            WHERE district_name = %s
            """,
            (district,)
        )

        result = cur.fetchone()

        if not result:
            skipped += 1
            continue

        district_id = result[0]

        incident_date = pd.to_datetime(
            row["Incident on"],
            dayfirst=True,
            errors="coerce"
        )

        if pd.isna(incident_date):
            skipped += 1
            continue

        cur.execute(
            """
            INSERT INTO heavy_rainfall_incidents (
                district_id,
                incident_date,
                estimated_loss_npr,
                house_destroyed,
                house_affected,
                livestock_destroyed,
                people_death,
                people_missing,
                people_injured
            )
            VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s
            )
            """,
            (
                district_id,
                incident_date.date(),

                safe_float(
                    row["Total estimated loss (NPR)"]
                ),

                safe_int(
                    row["House destroyed"]
                ),

                safe_int(
                    row["House affected"]
                ),

                safe_int(
                    row["Total livestock destroyed"]
                ),

                safe_int(
                    row["Total - People Death"]
                ),

                safe_int(
                    row["Total - People Missing"]
                ),

                safe_int(
                    row["Total - People Injured"]
                )
            )
        )

        inserted += 1

        if inserted % 500 == 0:
            conn.commit()
            print(f"Processed {inserted:,} rows...")

    conn.commit()

    cur.close()
    conn.close()

    print()
    print(f"Inserted : {inserted}")
    print(f"Skipped  : {skipped}")


if __name__ == "__main__":
    main()