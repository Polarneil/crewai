from google.cloud import bigquery
from langchain_community.tools import tool


# @tool("BigQuery Metadata Tool")
class BigQueryMetadataCatalogTool:
    """ Useful for retrieving BigQuery metadata from Google Cloud """
    def __init__(self, gcp_project, gcp_dataset, gcp_table):
        self.project_id = gcp_project
        self.dataset_id = gcp_dataset
        self.table_id = gcp_table
        self.client = bigquery.Client()

    def get_table_metadata(self):
        table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
        table = self.client.get_table(table_ref)

        table_metadata = {
            "table_id": table.table_id,
            "table_type": table.table_type,
            "full_table_id": table.full_table_id,
            "dataset_id": table.dataset_id,
            "description": table.description,
            "num_rows": table.num_rows,
            "created": str(table.created),
            "modified": str(table.modified),
            "expires": str(table.expires),
            "path": table.path,
        }

        field_metadata = []  # Store schema information here

        for schema_field in table.schema:
            field_info = {
                "Name": schema_field.name,
                "Type": schema_field.field_type,
                "Mode": schema_field.mode,
            }

            if schema_field.description:
                field_info["Description"] = schema_field.description

            if schema_field.fields:
                field_info["Fields"] = self.get_nested_fields(schema_field)

            if schema_field.precision is not None:
                field_info["Precision"] = schema_field.precision
            if schema_field.scale is not None:
                field_info["Scale"] = schema_field.scale

            field_metadata.append(field_info)  # Add field info to the list

        return table_metadata, field_metadata  # Return the list of dictionaries

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
