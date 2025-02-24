import os
from crewai import Crew

from textwrap import dedent
from agents import SQLAgents
from tasks import SQLTasks
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Create knowledge source
directions = "You will NOT include triple backticks (```) in any of your inputs or outputs."
direction_source = StringKnowledgeSource(
    content=directions,
)


class CustomCrew:
    def __init__(self, user_question):
        self.user_question = user_question

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = SQLAgents()
        tasks = SQLTasks()

        # Define your custom agents and tasks here
        sql_agent = agents.sql_agent()
        interpreter_agent = agents.interpreter_agent()

        # Custom tasks include agent name and variables as input
        generate_sql_script_task = tasks.generate_sql_script_task(
            sql_agent, user_question=self.user_question
        )

        execute_sql_script_task = tasks.execute_sql_script_task(
            sql_agent
        )

        generate_insights_task = tasks.generate_insights_task(
            interpreter_agent, self.user_question
        )

        # Define your custom crew here
        crew = Crew(
            agents=[sql_agent, interpreter_agent],
            tasks=[generate_sql_script_task, execute_sql_script_task, generate_insights_task],
            verbose=True,
            knowledge_sources=[direction_source],
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
