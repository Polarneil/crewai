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

    def retrieve_pg_data_task(self, agent, user_question):
        return Task(
            description=dedent(
                f"""
                Your task is to retrieve data from the postgres database to answer the user's question.
                
                You will utilize the schema returned from the previous task to familiarize yourself with the database.
                
                You will utilize the `pg_search_tool` function and pass in the appropriate table name that you 
                wish to retrieve data for, as well as the query you wish to run against the table you selected.
                                                
                User question: {user_question}
                """
            ),
            expected_output="The expected output of this task is data to support the user's question.",
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
