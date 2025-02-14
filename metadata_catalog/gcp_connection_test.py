"""
GCP connection instructions:

1. Install dependencies:
    - `pip install --upgrade google-cloud-bigquery`

2. Set up authentication
    - Install the Google Cloud CLI: https://cloud.google.com/sdk/docs/install
    - Extracts the contents of the zip to your root Home folder
    - Run installation script from the folder you extracted the zip to
        - `./google-cloud-sdk/install.sh`
    - Initialize the CLI by running:
        - `gcloud init`
    - Create authentication credentials for your local machine by running:
        - `gcloud auth application-default login`
"""

import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

os.environ["GCLOUD_PROJECT"] = os.getenv("GCP_PROJECT")

client = bigquery.Client()

query = """
SELECT * FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170801` LIMIT 10
"""

query_job = client.query(query)

results = query_job.result()

for row in results:
    print(row)
