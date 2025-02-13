import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv
from langchain_community.tools import tool

load_dotenv()

# PostgreSQL connection info
DB_CONFIG = {
    "user": os.getenv("PG_USERNAME"),
    "password": os.getenv("PG_PASSWORD"),
    "host": os.getenv("PG_HOST"),
    "port": os.getenv("PG_PORT")
}


@tool("Query Database")
def execute_query(sql_query: str):
    """ Useful for executing SQL queries on the database """
    query = f"""{sql_query}"""

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]  # Get column names

        df = pd.DataFrame(result, columns=column_names)  # Convert to pandas df
        return df

    except Exception as e:
        return {"error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
