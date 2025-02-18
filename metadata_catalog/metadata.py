from google.cloud import bigquery
import inspect
import os
from dotenv import load_dotenv

load_dotenv()

client = bigquery.Client()


def get_table_metadata(project_id, dataset_id, table_id):
    """Retrieves metadata for a BigQuery table."""
    try:
        table_ref = f"{project_id}.{dataset_id}.{table_id}"  # Construct table reference
        table = client.get_table(table_ref)  # API Request

        print("Schema:")
        for schema_field in table.schema:
            field_info = {
                "Name": schema_field.name,
                "Type": schema_field.field_type,
                "Mode": schema_field.mode,
            }

            if schema_field.description:
                field_info["Description"] = schema_field.description

            if schema_field.fields:
                field_info["Fields"] = []
                for nested_field in schema_field.fields:
                    nested_info = {
                        "Name": nested_field.name,
                        "Type": nested_field.field_type,
                        "Mode": nested_field.mode,
                    }
                    if nested_field.description:
                        nested_info["Description"] = nested_field.description

                    if nested_field.fields:  # Handle nested records recursively
                        nested_info["Fields"] = get_nested_fields(nested_field)

                    if nested_field.precision is not None:
                        nested_info["Precision"] = nested_field.precision
                    if nested_field.scale is not None:
                        nested_info["Scale"] = nested_field.scale
                    field_info["Fields"].append(nested_info)

            if schema_field.precision is not None:
                field_info["Precision"] = schema_field.precision
            if schema_field.scale is not None:
                field_info["Scale"] = schema_field.scale

            print(field_info)
            print("-" * 20)  # Separator between fields


        return table  # Return the Table object for further use

    except Exception as e:
        print(f"Error retrieving table metadata: {e}")
        return None


def get_nested_fields(schema_field):  # Recursive function to handle nested records
    nested_fields_list = []
    for nested_field in schema_field.fields:
        nested_info = {
            "Name": nested_field.name,
            "Type": nested_field.field_type,
            "Mode": nested_field.mode,
        }
        if nested_field.description:
            nested_info["Description"] = nested_field.description

        if nested_field.fields:  # Handle nested records recursively
            nested_info["Fields"] = get_nested_fields(nested_field)

        if nested_field.precision is not None:
            nested_info["Precision"] = nested_field.precision
        if nested_field.scale is not None:
            nested_info["Scale"] = nested_field.scale

        nested_fields_list.append(nested_info)
    return nested_fields_list


def get_dataset_tables(project_id, dataset_id):
  """Lists all tables in a dataset."""
  try:
      dataset_ref = f"{project_id}.{dataset_id}"
      tables = client.list_tables(dataset_ref)  # API request

      print(f"Tables in dataset {dataset_ref}:")
      for table in tables:
          print(f"- {table.table_id} ({table.table_type})")
      return tables

  except Exception as e:
      print(f"Error listing tables in dataset: {e}")
      return None


def get_project_datasets(project_id):
    """Lists all datasets in a project."""
    try:
        datasets = client.list_datasets(project_id)  # API request

        print(f"Datasets in project {project_id}:")
        for dataset in datasets:
            print(f"- {dataset.dataset_id}")
        return datasets

    except Exception as e:
        print(f"Error listing datasets in project: {e}")
        return None


# Example usage:
project_id = "bigquery-public-data"
dataset_id = "google_analytics_sample"
table_id = "ga_sessions_20170801"

get_table_metadata(project_id, dataset_id, table_id)

# get_dataset_tables(project_id, dataset_id)
#
# get_project_datasets(project_id)
