import sqlite3
import requests
# LangChain utility to interact with SQL databases
from langchain_community.utilities.sql_database import SQLDatabase
# SQLAlchemy function to create an engine
from sqlalchemy import create_engine
# SQLAlchemy connection pool class for in-memory databases
from sqlalchemy.pool import StaticPool

def get_engine_for_chinook_db() -> create_engine:
    """
    Returns a SQLAlchemy engine for the Chinook database.
    
    This function creates an in-memory SQLite database engine that uses a static pool,
    which is suitable for testing and development purposes.
    
    Returns:
        create_engine: A SQLAlchemy engine connected to the Chinook database.
    """
    url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"

    response = requests.get(url)
    sql_script = response.text

    # Create an in-memory SQLite database and execute the SQL script to set it up
    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.executescript(sql_script)

    # Create a SQLAlchemy engine that uses the in-memory SQLite database
    # `creator=lambda: connection` tells SQLAlchemy to use the existing SQLite connection
    # `check_same_thread=False` allows the same thread to use the connection
    # `connect_args` is set to allow the same thread to use the connection
    # `poolclass=StaticPool` is set to StaticPool to avoid issues with SQLite's threading model
    return create_engine(
        "sqlite://",
        creator=lambda: connection,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

def get_chinook_db() -> SQLDatabase:
    """
    Returns a SQLDatabase instance connected to the Chinook database.
    
    This function creates a SQLAlchemy engine for the Chinook database and then
    returns a SQLDatabase instance that can be used to interact with the database.
    
    Returns:
        SQLDatabase: An instance of SQLDatabase connected to the Chinook database.
    """
    engine = get_engine_for_chinook_db()
    return SQLDatabase(engine=engine)