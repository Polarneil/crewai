import os
from crewai import Crew

from textwrap import dedent
from agents import SQLAgents
from tasks import SQLTasks

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class CustomCrew:
    def __init__(self, user_question):
        self.user_question = user_question

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = SQLAgents()
        tasks = SQLTasks()

        # Define your custom agents and tasks here
        schema_agent = agents.schema_agent()
        sql_agent = agents.sql_agent()
        interpreter_agent = agents.interpreter_agent()

        # Custom tasks include agent name and variables as input
        fetch_schema_task = tasks.fetch_schema_task(
            schema_agent
        )

        retrieve_pg_data_task = tasks.retrieve_pg_data_task(
            sql_agent, user_question=self.user_question
        )

        generate_insights_task = tasks.generate_insights_task(
            interpreter_agent, self.user_question
        )

        # Define your custom crew here
        crew = Crew(
            agents=[schema_agent, sql_agent, interpreter_agent],
            tasks=[fetch_schema_task, retrieve_pg_data_task, generate_insights_task],
            verbose=True,
        )

        result = crew.kickoff()
        return result


# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    print("## Welcome to SQL Crew AI Template")
    print("-------------------------------")
    user_question = input(dedent("""Enter a question about your data: """))

    custom_crew = CustomCrew(user_question)
    result = custom_crew.run()
    print("\n\n########################")
    print("## Here is you SQL crew run result:")
    print("########################\n")
    print(result)
