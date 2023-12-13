from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from asyncpg.exceptions import UndefinedTableError
import databases
import asyncpg
from . import constants as const


#### DATABASE MODELS ####
## Users
metadata = MetaData()
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("email", String, unique=True, index=True),
    Column("username", String, unique=True, index=True),
    Column("password", String),
    Column("grant_type", String),
)


### DB Class
class db:
    def __init__(self):
        self.database_url = const.DATABASE_URL
        self.engine = create_engine(self.database_url, echo=True, implicit_returning=True)
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
        metadata.create_all(self.engine)




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
