from crewai import Agent, LLM
from textwrap import dedent
from dotenv import load_dotenv
import os

load_dotenv()


# This is an example of how to define custom agents.
# You can define as many agents as you want.
# You can also define custom tasks in tasks.py
class CustomAgents:
    def __init__(self):
        self.OpenAIGPT35 = LLM(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.OpenAIGPT4o = LLM(
            model="gpt-4o",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.Gemini2Flash = LLM(
            model='gemini/gemini-2.0-flash',
            api_key=os.getenv("GEMINI_API_KEY"),
        )
        self.Ollama = LLM(
            model="ollama/llama3.1:8b",
            base_url="http://localhost:11434",
        )

    def agent_1_name(self):
        return Agent(
            role="Define agent 1 role here",
            backstory=dedent(f"""Define agent 1 backstory here"""),
            goal=dedent(f"""Define agent 1 goal here"""),
            # tools=[tool_1, tool_2],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4o,
        )

    def agent_2_name(self):
        return Agent(
            role="Define agent 2 role here",
            backstory=dedent(f"""Define agent 2 backstory here"""),
            goal=dedent(f"""Define agent 2 goal here"""),
            # tools=[tool_1, tool_2],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4o,
        )
