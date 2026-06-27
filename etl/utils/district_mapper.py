from sqlalchemy import text

from database.db_connection import DatabaseConnection


class DistrictMapper:
    """
    Resolves district names to district IDs.

    Checks:
    1. districts table
    2. district_aliases table

    Returns district_id if found.
    """

    def __init__(self):
        self.engine = DatabaseConnection().get_engine()

        self.district_cache = {}
        self.alias_cache = {}

        self._load_cache()

    def _load_cache(self):

        with self.engine.connect() as connection:

            districts = connection.execute(
                text("""
                    SELECT district_id,
                           district_name
                    FROM districts
                """)
            )

            for row in districts:
                self.district_cache[
                    row.district_name.strip().lower()
                ] = row.district_id

            aliases = connection.execute(
                text("""
                    SELECT alias_name,
                           district_id
                    FROM district_aliases
                """)
            )

            for row in aliases:
                self.alias_cache[
                    row.alias_name.strip().lower()
                ] = row.district_id

    def get_district_id(self, district_name):

        if district_name is None:
            return None

        name = district_name.strip().lower()

        if name in self.district_cache:
            return self.district_cache[name]

        if name in self.alias_cache:
            return self.alias_cache[name]

        return None