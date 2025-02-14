from crewai import Task
from textwrap import dedent


class SQLTasks:

    def fetch_schema_task(self, agent):
        return Task(
            description=dedent(
                f"""
                Your task is to analyze a databases schema and return the details for a SQL Agent to leverage.
                
                The SQL agent's job is to turn natural language questions about the database into a SQL query and the 
                agent will need a detailed schema report to do this.
                
                Your job is to return a report of the schema to enable the SQL agent. You will utilize the help of tools
                I give you to run queries against the database and retrieve schema information.
                """
            ),
            expected_output="You will return a list of json objects just as the query returns to you.",
            agent=agent,
        )

    def generate_sql_script_task(self, agent, user_question):
        return Task(
            description=dedent(
                f"""
                Your task is to generate a SQL script based on the user's input question. You will leverage the schema
                returned from the schema agent.
                
                The SQL script should be executable against the database and fit with the schema. This script should be 
                created with the users question in mind. The data returned from this executable SQL script should be 
                answer the user's question.
                
                Note: timestamp fields must be querired like this (example):
                
                SELECT * FROM api_visitorlog 
                WHERE timestamp::text LIKE '2025-01-21%';
                
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
