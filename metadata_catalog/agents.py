from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from BigQueryTool import get_table_metadata


class CustomAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4o = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
        self.Ollama = ChatOpenAI(
            model="ollama/llama3.1:8b",
            base_url="http://localhost:11434"
        )

    def gcp_warehouse_metadata(self):
        return Agent(
            role="Google Cloud Engineer",
            backstory=dedent(f"""You have spend your entire professional career in the Google Cloud environment."""),
            goal=dedent(f"""Define agent 1 goal here"""),
            tools=[get_table_metadata],
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
