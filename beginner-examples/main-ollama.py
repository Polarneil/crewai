import time
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI


start_time = time.perf_counter()

llm = ChatOpenAI(
    model="ollama/llama3.1:8b",
    base_url="http://localhost:11434"
)


# Create the Agent
info_agent = Agent(
    role="Information Agent",
    goal="Give compelling information about a certain topic.",
    backstory="""
    You love to know information. People love and hate you for it. You win most of the quizzes at your local pub.
    """,
    llm=llm  # point to the local model
)

task_1 = Task(
    description="Tell me all about the box jelly fish.",
    expected_output="Give me a quick summary and then also give me 7 bullet points describing it.",
    agent=info_agent
)

crew = Crew(
    agents=[info_agent],
    tasks=[task_1],
    verbose=True  # Since verbose is true, we don't need to print the output
)

result = crew.kickoff()

end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
