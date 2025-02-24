import json
from langchain_community.tools import tool


@tool("MetadataSchemaTool")
def get_schema(filepath):
    """ Useful for retrieving database schema information """
    try:
        with open(filepath, 'r') as file:
            schema_metadata = json.load(file)
            return schema_metadata
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filepath}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
