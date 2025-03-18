from db_config import Base
from sqlalchemy.exc import OperationalError
from fastapi import HTTPException
from sqlalchemy import inspect
from db_config import engine

Base.metadata.create_all(bind=engine)


def check_and_create_table(db_engine):
    try:
        tables_list = list(Base.metadata.tables.keys())
        inspector = inspect(db_engine)  # Use inspect() to inspect the engine

        # Check if each table exists
        for table_name in tables_list:
            if table_name not in inspector.get_table_names():
                print(f"Table '{table_name}' does not exist, creating it...")
                # Create the table if it doesn't exist
                Base.metadata.create_all(bind=db_engine)
            else:
                print(f"Table '{table_name}' already exists.")

    except OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

