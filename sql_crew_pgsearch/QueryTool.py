import os
from dotenv import load_dotenv
from langchain_community.tools import tool
from crewai_tools import PGSearchTool

load_dotenv()

# PostgreSQL connection info
DB_CONFIG = {
    "user": os.getenv("PG_USERNAME"),
    "password": os.getenv("PG_PASSWORD"),
    "host": os.getenv("PG_HOST"),
    "port": os.getenv("PG_PORT"),
    "database": os.getenv("DATABASE")
}


# @tool("Query Database")
def pg_search_tool(table_name, query):
    """
    Useful for retrieving data from PostgreSQL database tables.

    Args:
        table_name: The name of the table to query (string).
        query: The SQL query to execute (string).  Should be compatible with the specified table.
    """
    db_uri = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

    tool = PGSearchTool(
        db_uri=db_uri,
        table_name=table_name,
    )

    try:
        results = tool.run(query)
        return results  # Process results as needed. They'll be a list of dictionaries.
    except Exception as e:
        print(f"Error during database search: {e}")
        return None


print(pg_search_tool("api_visitorlog", "iPhone"))
