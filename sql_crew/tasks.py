from crewai import Task
from textwrap import dedent


class SQLTasks:

    def generate_sql_script_task(self, agent, user_question):
        return Task(
            description=dedent(
                f"""
                Your task is to generate a SQL script based on the user's input question. You will leverage the schema
                to formulate this query. You will utilize the `MetadataSchemaTool`, calling the `get_schema` function
                 and passing in the file path '../metadata_catalog/catalog_outputs/metadata_catalog.json' to get the
                 schema.
                
                The SQL script should be executable against the database and fit with the schema. This script should be 
                created with the users question in mind. The data returned from this executable SQL script should be 
                answer the user's question.
                                
                Note: If a user enters a question related to the current date (ex. "show me data from the past week"),
                utilize the `get_date_time` tool function.
                                                
                User question: {user_question}
                """
            ),
            expected_output="""The expected output of this task is a SQL script in string format to pass into a 
            function. There should be no triple back ticks in your output""",
            agent=agent,
        )

    def execute_sql_script_task(self, agent):
        return Task(
            description=dedent(
                f"""
                Your task is to execute the SQL script provided as a result from the `generate_sql_script_task`.
                
                You will reference the `execute_query` function from the `execute_query` tool that you were provided.
                This function takes in a SQL script as a string and returns a pandas df on the results.
                
                Your job is to pass the SQL script returned from the prior task into this function and execute it.
                """
            ),
            expected_output="The expected output of this task is the pandas df returned from the execution of the query",
            agent=agent,
        )

    def generate_insights_task(self, agent, user_question):
        return Task(
            description=dedent(
                f"""
                Your task is to examine the data returned from the SQL agent and generate insights that will be helpful
                to the user based on their initial question, which you will find below.
                
                User's inital question: {user_question}
                """
            ),
            expected_output=""""The expected output of this task is the generated insights as well as the raw pandas 
            df that was returned from the SQL agent.""",
            agent=agent,
        )
