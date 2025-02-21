import os
from crewai import Crew
from agents import GCPAgents
from tasks import GCPTasks
from dotenv import load_dotenv
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
project_id = os.getenv("GCP_PROJECT_DEMO")

# Create knowledge source
directions = "You will NOT include triple backticks (```) in any of your inputs or outputs."
direction_source = StringKnowledgeSource(
    content=directions,
)


class CloudCrew:
    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = GCPAgents()
        tasks = GCPTasks()

        # Define your custom agents and tasks here
        gcp_warehouse_agent = agents.gcp_warehouse_agent()

        gcp_metadata_agent = agents.gcp_metadata_agent()

        # Custom tasks include agent name and variables as input
        scan_warehouse_task = tasks.get_datasets_tables_task(
            agent=gcp_warehouse_agent,
            project_id=project_id,
        )

        extract_metadata_task = tasks.extract_metadata_task(
            agent=gcp_metadata_agent,
        )

        # Define your custom crew here
        crew = Crew(
            agents=[gcp_warehouse_agent, gcp_metadata_agent],
            tasks=[scan_warehouse_task, extract_metadata_task],
            knowledge_sources=[direction_source],
            verbose=True,
        )

        result = crew.kickoff()
        return result


# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    print("## Welcome to CloudCrew AI Metadata Catalog")
    print("-------------------------------")

    cloud_crew = CloudCrew()
    result = cloud_crew.run()
    print("\n########################")
    print("## Here is you cloud crew run result:")
    print("########################\n")
    print(result)
