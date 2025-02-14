from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from SchemaTool import get_schema
from QueryTool import pg_search_tool


class SQLAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4o = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
        self.Ollama = ChatOpenAI(
            model="ollama/llama3.1:8b",
            base_url="http://localhost:11434"
        )

    def schema_agent(self):
        return Agent(
            role="Database Schema Analyst",
            backstory=dedent(f"""
            You have been a Database Schema Analyst your entire life. You generate database schema reports constantly.
            """),
            goal=dedent(f"""Your goal will to return schema details from a database."""),
            tools=[get_schema],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4o,
        )

    def sql_agent(self):
        return Agent(
            role="PostgreSQL Database Engineer",
            backstory=dedent(f"""You have spent you entire career quickly and efficiently retrieving data from postgres
            databases. You can answer any question."""),
            goal=dedent(f"""Your goal is to answer natural language questions with data from PostgreSQL databases."""),
            tools=[pg_search_tool],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4o,
        )

    def interpreter_agent(self):
        return Agent(
            role="Data Interpreter",
            backstory=dedent(f"""You are known as a brilliant interpreter of data"""),
            goal=dedent(f"""Your goal is to interpret data returned from a the SQL agent's query and use it to answer  
            the users question"""),
            allow_delegation=False,
            verbos=True,
            llm=self.OpenAIGPT4o,
        )
