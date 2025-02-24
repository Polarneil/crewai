import os
from google.cloud import bigquery
from langchain_community.tools import tool
from dotenv import load_dotenv

load_dotenv()

os.environ["GCLOUD_PROJECT"] = os.getenv("GCP_PROJECT")


@tool("MetadataQueryTool")
def execute_query(sql_query: str):
    """ Useful for executing SQL queries on the database """
    try:
        client = bigquery.Client()
        query_job = client.query(sql_query)
        results = query_job.result()
        df = results.to_dataframe(create_bqstorage_client=False)  # Added create_bqstorage_client = False
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
