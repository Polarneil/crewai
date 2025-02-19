from crewai import Task
from textwrap import dedent


class GCPTasks:
    def analyze_warehouse_task(self, agent):
        return Task(
            description=dedent(
                f"""
                Your task is to collect and metdata in a metadata catalog from Google Cloud's BigQuery using the
                `BigQuery Metadata Tool`. This tool returns table and field metadata that will be useful in your
                creation of a metadata catalog.
                
                You will use the `catalog_example_knowledge` as an example of how to format a metadata catalog.    
                """
            ),
            expected_output="The expected output of the task is a metadata catalog.",
            output_file="metadata_catalog.json",
            agent=agent,
        )
