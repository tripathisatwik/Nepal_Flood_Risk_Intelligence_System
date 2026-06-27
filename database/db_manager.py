from pathlib import Path
import pandas as pd
from sqlalchemy import text
from database.db_connection import DatabaseConnection
import pandas as pd

class DatabaseManager:

    def __init__(self):
        self.engine = DatabaseConnection().get_engine()

    def create_schema(self):
        schema_file = Path("database/schema.sql")

        with open(schema_file, "r", encoding="utf-8") as file:
            sql_script = file.read()

        with self.engine.connect() as connection:
            connection.execute(text(sql_script))
            connection.commit()

        print("Database schema created successfully.")

    def test_connection(self):
        with self.engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))

            for row in result:
                print(row[0])

    def execute_query(self, query, params=None):
        with self.engine.connect() as connection:
            connection.execute(text(query), params or {})
            connection.commit()

    def fetch_all(self, query, params=None):
        with self.engine.connect() as connection:
            result = connection.execute(text(query), params or {})
            return result.fetchall()

    def fetch_one(self, query, params=None):
        with self.engine.connect() as connection:
            result = connection.execute(text(query), params or {})
            return result.fetchone()

    def read_query(self, query):
        with self.engine.connect() as connection:
            return pd.read_sql(query, connection)

    def execute_query(self, query):
           with self.engine.connect() as connection:
            connection.execute(text(query))
            connection.commit()

    def write_dataframe(self,dataframe,table_name):
        dataframe.to_sql(
            table_name,
            self.engine,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=5000
        )       

    def fetch_dataframe(self,query):

        return pd.read_sql(
            query,
            self.engine
        )