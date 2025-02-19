from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from BigQueryTool import BigQueryMetadataCatalogTool
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource

# knowledge source
catalog_example_knowledge = JSONKnowledgeSource(
    file_paths=["/catalog_example.json"]
)


class GCPAgents:
    def __init__(self, gcp_project, gcp_dataset, gcp_table):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4o = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
        self.Ollama = ChatOpenAI(
            model="ollama/llama3.1:8b",
            base_url="http://localhost:11434"
        )
        self.bigquery_tool = BigQueryMetadataCatalogTool(
            gcp_project=gcp_project,
            gcp_dataset=gcp_dataset,
            gcp_table=gcp_table,
        )

    def gcp_warehouse_agent(self):
        return Agent(
            role="Google Cloud Engineer",
            backstory=dedent(f"""You have spend your entire professional career in the Google Cloud environment."""),
            goal=dedent(f"""Your goal is to collect and organize metadata from Google Cloud's BigQuery."""),
            tools=[self.bigquery_tool],
            knowledge_sources=[catalog_example_knowledge],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4o,
        )
