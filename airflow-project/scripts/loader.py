import sys
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://airflow:airflow@postgres:5432/postgres")


        
def create_schema(schema_name):
    ALLOWED_SCHEMAS = {"bronze_layer","silver_layer","gold_layer"}

    if schema_name not in ALLOWED_SCHEMAS:
        raise ValueError(
            f"Invalid schema '{schema_name}'. "
            f"Allowed values are: {ALLOWED_SCHEMAS}")

    with engine.begin() as conn:
        conn.execute(
            text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
        )

def write_to_db(data_df, table_name, mode,schema):
    """
    schema : bronze_layer, silver_layer, gold_layer
    mode : append or replace
    """
    create_schema(schema_name = schema)
    data_df.to_sql(
    name=table_name,
    con=engine,
    schema=schema,
    if_exists=mode,
    index=False)

def read_df(query):
    data_df = pd.read_sql(query, engine)
    return data_df
