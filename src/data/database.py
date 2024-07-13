from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from asyncpg.exceptions import UndefinedTableError
import databases
import asyncpg
import pandas as pd
from . import tables




### DB Class
class db:
    def __init__(self):
        self.engine = tables.engine
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_db(self):
        try:
            conn = self.engine.connect()
            return conn

        except UndefinedTableError as UTError:
            print("Error: ", UTError)

    def db_query(self, query):
        result = self.session.execute(query)
        return result

    def update_tables(self):
        tables.declarative_base_metadata.create_all(self.engine)

    def get_session(self):
        return self.session

    def import_table_from_file(self, table_name, df):
        try: 
            print(df)
            df.to_sql(table_name, con=self.engine, if_exists='replace', index=False)
            with self.engine.connect() as connection:
                connection.execute(f'ALTER TABLE {table_name} ADD PRIMARY KEY (id);')

            return True
        except Exception:
            return None

# async def main():
#     database_url = "postgresql://postgres:123456@localhost:5412"
#     database = databases.Database(database_url)
#     await database.connect()
#     if not database.is_connected:
#         raise ConnectionError("Could not connect to database")
#     results = await database.fetch_all(query="SELECT * FROM users")
#     print(results)
#     await database.disconnect()

# asyncio.run(main())
