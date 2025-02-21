from crewai import Task
from textwrap import dedent


class GCPTasks:
    def get_datasets_tables_task(self, agent, project_id):
        return Task(
            description=dedent(
                f"""
                You will call the `list_datasets_and_tables` function from the `DatasetsTablesTool` tool passing in 
                the project id into the function as a string. You can find the project id below:
                
                project_id={project_id}
                """
            ),
            expected_output=dedent(
                f"""
                The expected output of this task is the file path that is returned from the `DatasetsTablesTool`.
                tool.
                """
            ),
            agent=agent,
        )

    def extract_metadata_task(self, agent):
        return Task(
            description=dedent(
                f"""
                You will call the `get_table_metadata` function from the `BigQuery Metadata Tool`. You will pass in the
                file path returned from the task `get_datasets_tables_task`.
                """
            ),
            expected_output=dedent(
                f"""
                The expected output of this task is a success or fail message that will be derived from the output of
                the `get_table_metadata` function from the `BigQuery Metadata Tool.
                """
            ),
            agent=agent,
        )
