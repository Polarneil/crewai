from google.cloud import bigquery
from langchain_community.tools import tool
import json
import os
from dotenv import load_dotenv
from textwrap import dedent

load_dotenv()

gcp_proj = os.getenv("GCP_PROJECT_DEMO")

client = bigquery.Client()


def update_version(current_version):
    """Helper function to increment version number"""
    major, minor = map(int, current_version.split('.'))
    minor += 1
    if minor > 9:
        major += 1
        minor = 0
    return f"{major}.{minor}"


@tool("BigQuery Metadata Tool")
def get_table_metadata(dataset_table_data_path: str):
    """ Useful for retrieving BigQuery metadata from Google Cloud """

    datasets_added = 0
    datasets_updated = 0
    datasets_skipped = 0
    tables_added = 0
    tables_updated = 0
    tables_skipped = 0

    filepath = './catalog_outputs/metadata_catalog.json'

    # Load or initialize catalog data once at the start
    try:
        with open(filepath, 'r') as catalog_json_file:
            catalog_data = json.load(catalog_json_file)
    except FileNotFoundError:
        catalog_data = {
            "catalog_name": "FallBackCatalog",
            "description": "A fallback metadata catalog for a data warehouse.",
            "version": "1.0",
            "data_assets": []
        }

    # Update version once per run
    current_version = catalog_data.get("version", "1.0")
    catalog_data["version"] = update_version(current_version)

    with open(dataset_table_data_path, 'r') as dataset_table_file:
        dataset_table_data = json.load(dataset_table_file)

    # Process all datasets and tables
    for dataset, tables in dataset_table_data.items():
        dataset_ref = f"{gcp_proj}.{dataset}"
        dataset_obj = client.get_dataset(dataset_ref)

        dataset_metadata = {
            "dataset_id": dataset_obj.dataset_id,
            "description": dataset_obj.description,
            "data_location": dataset_obj.location,
            "created": str(dataset_obj.created),
            "modified": str(dataset_obj.modified),
            "path": dataset_obj.path,
            "data_assets": [],
        }

        found_dataset = False
        dataset_index = -1
        for i, asset in enumerate(catalog_data["data_assets"]):
            if asset["dataset_id"] == dataset_metadata["dataset_id"]:
                found_dataset = True
                dataset_index = i
                if asset["modified"] != dataset_metadata["modified"]:
                    catalog_data["data_assets"][i] = dataset_metadata
                    datasets_updated += 1
                else:
                    datasets_skipped += 1
                break

        if not found_dataset:
            catalog_data["data_assets"].append(dataset_metadata)
            datasets_added += 1
        else:
            dataset_metadata = catalog_data["data_assets"][dataset_index]

        for table in tables:
            if table == "ga_sessions_20170801" or table == "ga_sessions_20170731":  # FILTERED DOWN TABLES FOR TESTING
                table_ref = f"{gcp_proj}.{dataset}.{table}"
                table_obj = client.get_table(table_ref)

                table_metadata = {
                    "asset_type": table_obj.table_type,
                    "table_id": table_obj.table_id,
                    "full_table_id": table_obj.full_table_id,
                    "dataset_id": table_obj.dataset_id,
                    "description": table_obj.description,
                    "num_rows": table_obj.num_rows,
                    "created": str(table_obj.created),
                    "modified": str(table_obj.modified),
                    "expires": str(table_obj.expires),
                    "path": table_obj.path,
                }

                field_metadata = []

                for schema_field in table_obj.schema:
                    field_info = {
                        "Name": schema_field.name,
                        "Type": schema_field.field_type,
                        "Mode": schema_field.mode,
                    }

                    if schema_field.description:
                        field_info["Description"] = schema_field.description

                    if schema_field.fields:
                        field_info["Fields"] = get_nested_fields(schema_field)

                    if schema_field.precision is not None:
                        field_info["Precision"] = schema_field.precision
                    if schema_field.scale is not None:
                        field_info["Scale"] = schema_field.scale

                    field_metadata.append(field_info)

                table_metadata["columns"] = field_metadata

                found = False
                for i, asset in enumerate(dataset_metadata["data_assets"]):
                    if asset["full_table_id"] == table_metadata["full_table_id"]:
                        found = True
                        if asset["modified"] != table_metadata["modified"]:
                            dataset_metadata["data_assets"][i] = table_metadata
                            tables_updated += 1
                        else:
                            tables_skipped += 1
                        break

                if not found:
                    dataset_metadata["data_assets"].append(table_metadata)
                    tables_added += 1

    catalog_data["change_summary"] = {
        "datasets_added": datasets_added,
        "datasets_updated": datasets_updated,
        "datasets_skipped": datasets_skipped,
        "tables_added": tables_added,
        "tables_updated": tables_updated,
        "tables_skipped": tables_skipped
    }

    # Write the updated catalog once after all tables are processed
    with open(f"./catalog_outputs/metadata_catalog_{catalog_data['version']}.json", 'w') as catalog_json_file:
        json.dump(catalog_data, catalog_json_file, indent=4)

    with open(filepath, 'w') as catalog_json_file:
        json.dump(catalog_data, catalog_json_file, indent=4)

    success_message = dedent(
        f"""
        Summary:
        Catalog version: {catalog_data["version"]}
        Datasets added: {datasets_added}
        Datasets updated: {datasets_updated}
        Datasets skipped: {datasets_skipped}
        Tables added: {tables_added}
        Tables updated: {tables_updated}
        Tables skipped: {tables_skipped}
        """
    )

    return success_message


def get_nested_fields(schema_field):
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
