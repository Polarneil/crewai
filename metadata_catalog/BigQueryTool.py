from google.cloud import bigquery
from dotenv import load_dotenv
import json
import os

load_dotenv()

gcp_project = os.getenv("GCP_PROJECT_DEMO")
gcp_dataset = os.getenv("GCP_DATASET_DEMO")
gcp_table = os.getenv("GCP_TABLE_DEMO")


# Add the tool decorator and pass into the first Agent
class BigQueryMetadataCatalogTool:
    def __init__(self, project_id, dataset_id, table_id):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.client = bigquery.Client()

    def get_table_metadata(self):
        table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
        table = self.client.get_table(table_ref)

        schema_info = []  # Store schema information here

        for schema_field in table.schema:
            field_info = {
                "Name": schema_field.name,
                "Type": schema_field.field_type,
                "Mode": schema_field.mode,
            }

            if schema_field.description:
                field_info["Description"] = schema_field.description

            if schema_field.fields:
                field_info["Fields"] = self.get_nested_fields(schema_field) # Use self here, not classname

            if schema_field.precision is not None:
                field_info["Precision"] = schema_field.precision
            if schema_field.scale is not None:
                field_info["Scale"] = schema_field.scale

            schema_info.append(field_info)  # Add field info to the list

        return schema_info  # Return the list of dictionaries

    def get_nested_fields(self, schema_field):

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
                nested_info["Fields"] = self.get_nested_fields(nested_field)

            if nested_field.precision is not None:
                nested_info["Precision"] = nested_field.precision
            if nested_field.scale is not None:
                nested_info["Scale"] = nested_field.scale

            nested_fields_list.append(nested_info)
        return nested_fields_list


tooler = BigQueryMetadataCatalogTool(gcp_project, gcp_dataset, gcp_table)

metadata = tooler.get_table_metadata()  # Get the returned metadata

print(json.dumps(metadata, indent=4))
