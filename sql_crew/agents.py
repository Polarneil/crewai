from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
# from SchemaTool import get_schema
# from QueryTool import execute_query
from MetadataSchemaTool import get_schema
from MetadataQueryTool import execute_query
from DateTool import get_date_time


class SQLAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4o = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
        self.OpenAIGPT4omini = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
        self.Ollama = ChatOpenAI(
            model="ollama/llama3.1:8b",
            base_url="http://localhost:11434"
        )

    def sql_agent(self):
        return Agent(
            role="SQL Script Engineer",
            backstory=dedent(f"""You have spent your career writing and running the most cutting edge and accurate SQL
            scripts. You can write and run a SQL script to answer any question."""),
            goal=dedent(f"""Your goal is to turn natural language business questions into executable SQL scripts. You 
            will also run these scripts."""),
            tools=[get_schema, execute_query, get_date_time],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4omini,
        )

    def interpreter_agent(self):
        return Agent(
            role="Data Interpreter",
            backstory=dedent(f"""You are known as a brilliant interpreter of data"""),
            goal=dedent(f"""Your goal is to interpret data returned from a the SQL agent's query and use it to answer  
            the users question"""),
            allow_delegation=False,
            verbos=True,
            llm=self.OpenAIGPT4omini,
        )
