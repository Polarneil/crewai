import os
from crewai import Crew
from agents import GCPAgents
from tasks import GCPTasks
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

gcp_proj = os.getenv("GCP_PROJECT_DEMO")
gcp_dset = os.getenv("GCP_DATASET_DEMO")
gcp_tab = os.getenv("GCP_TABLE_DEMO")

class CloudCrew:
    def __init__(self, gcp_project, gcp_dataset, gcp_table):
        self.gcp_project = gcp_project
        self.gcp_dataset = gcp_dataset
        self.gcp_table = gcp_table

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = GCPAgents(gcp_project=self.gcp_project, gcp_dataset=self.gcp_dataset, gcp_table=self.gcp_table)
        tasks = GCPTasks()

        # Define your custom agents and tasks here
        gcp_warehouse_agent = agents.gcp_warehouse_agent()

        # Custom tasks include agent name and variables as input
        analyze_warehouse_task = tasks.analyze_warehouse_task(
            gcp_warehouse_agent,
        )

        # Define your custom crew here
        crew = Crew(
            agents=[gcp_warehouse_agent],
            tasks=[analyze_warehouse_task],
            verbose=True,
        )

        result = crew.kickoff()
        return result


# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    print("## Welcome to CloudCrew AI Metadata Catalog")
    print("-------------------------------")

    cloud_crew = CloudCrew(gcp_project=gcp_proj, gcp_dataset=gcp_dset, gcp_table=gcp_tab)
    result = cloud_crew.run()
    print("\n\n########################")
    print("## Here is you cloud crew run result:")
    print("########################\n")
    print(result)
