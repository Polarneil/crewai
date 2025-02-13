import os
from crewai import Agent, Task, Crew

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = os.getenv("OPENAI_MODEL_NAME")

# Create the Agent
info_agent = Agent(
    role="Information Agent",
    goal="Give compelling information about a certain topic.",
    backstory="""
    You love to know information. People love and hate you for it. You win most of the quizzes at your local pub.
    """
)

task_1 = Task(
    description="Tell me all about the blue-ringed octopus.",
    expected_output="Give me a quick summary and then also give me 7 bullet points describing it.",
    agent=info_agent
)

crew = Crew(
    agents=[info_agent],
    tasks=[task_1],
    verbose=True  # Since verbose is true, we don't need to print the output
)

result = crew.kickoff()
