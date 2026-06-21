from dotenv import load_dotenv
import os

from sqlalchemy import create_engine


class DatabaseConnection:
    """
    Handles PostgreSQL connection.
    """

    def __init__(self):
        load_dotenv()

        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        database = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")

        connection_string = (
            f"postgresql+psycopg2://"
            f"{user}:{password}@{host}:{port}/{database}"
        )

        self.engine = create_engine(connection_string)

    def get_engine(self):
        return self.engine