from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from DatasetsTablesTool import list_datasets_and_tables
from BigQueryTool import get_table_metadata


class GCPAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4o = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
        self.OpenAIGPT4omini = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
        self.Ollama = ChatOpenAI(
            model="ollama/llama3.1:8b",
            base_url="http://localhost:11434"
        )

    def gcp_warehouse_agent(self):
        return Agent(
            role="Google Cloud Engineer",
            backstory=dedent(f"""You have spend your entire professional career in the Google Cloud environment."""),
            goal=dedent(f"""Your goal is to collect and organize metadata from Google Cloud's BigQuery."""),
            tools=[list_datasets_and_tables],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4omini,
        )

    def gcp_metadata_agent(self):
        return Agent(
            role="Metadata Extractor",
            backstory=dedent(f"""You are an expert at extracting metadata from BigQuery tables."""),
            goal=dedent(f"""Your goal is to extract specific metadata from the tables provided."""),
            tools=[get_table_metadata],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4omini,
        )
