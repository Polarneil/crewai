import psycopg2
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


@tool("Schema Getter")
def get_schema():
    """ Useful for retrieving database schema information """
    query = """
    SELECT table_schema, table_name, column_name, data_type 
    FROM information_schema.columns 
    WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
    ORDER BY table_schema, table_name, ordinal_position;
    """

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(query)
        schema_info = cursor.fetchall()

        # Return structured schema info
        result = [
            {"schema": row[0], "table": row[1], "column": row[2], "type": row[3]}
            for row in schema_info
        ]
        return result

    except Exception as e:
        return {"error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
