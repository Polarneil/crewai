import json
from google.cloud import bigquery
from langchain_community.tools import tool
from dotenv import load_dotenv

load_dotenv()


@tool('DatasetsTablesTool')
def list_datasets_and_tables(project_id: str):
    """Lists all datasets and tables in a BigQuery project."""

    try:
        client = bigquery.Client(project=project_id)

        datasets_and_tables = {}

        datasets = client.list_datasets()  # API request
        for dataset in datasets:
            if dataset.dataset_id.lower() == "google_analytics_sample":  # FILTERED DOWN DATASETS FOR TESTING (filtered the tables on line 57 of BigQueryTool.py)
                dataset_id = dataset.dataset_id
                datasets_and_tables[dataset_id] = []
            else:
                continue

            try:
                tables = client.list_tables(dataset_id)  # API request
                for table in tables:
                    datasets_and_tables[dataset_id].append(table.table_id)
            except Exception as table_error:
                print(f"Error listing tables in dataset {dataset_id}: {table_error}")

        filename = "./staging/datasets_and_tables.json"

        with open(filename, 'w') as f:
            json.dump(datasets_and_tables, f, indent=4)

        return filename

    except Exception as project_error:
        print(f"Error listing datasets for project {project_id}: {project_error}")
        return {}
