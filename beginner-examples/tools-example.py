import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from CalculatorTool import calculate

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = os.getenv("OPENAI_MODEL_NAME")

math_input = input("Enter math equation: ")

math_agent = Agent(
    role="Math Magician",
    goal="You are able to evaluate any math expression.",
    backstory="You are a math WHIZ.",
    verbose=True,
    tools=[calculate]
)

writer = Agent(
    role="Writer",
    goal="Craft compelling explanations based from results of math equations.",
    backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
    You transform complex concepts into compelling narratives.
    """,
    verbose=True
)

task_1 = Task(
    description=f"{math_input}",
    expected_output="Give full details in bullet points.",
    agent=math_agent
)

task_2 = Task(
    description="Using the insights provided, explain in great detail how the equation and result were formed.",
    expected_output="""Explain in great detail and save in markdown. Do not add triple tick marks at the beginning or end of the file.
    Also don't say what type it is in the first line
    """,
    output_file="math.md",  # path traversals are now allowed here
    agent=writer
)

crew = Crew(
    agents=[math_agent, writer],
    tasks=[task_1, task_2],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()
