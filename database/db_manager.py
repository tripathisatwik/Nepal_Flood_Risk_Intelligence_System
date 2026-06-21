from pathlib import Path

from sqlalchemy import text

from database.db_connection import DatabaseConnection


class DatabaseManager:
    """
    Creates database tables
    and performs basic checks.
    """

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