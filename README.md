# gcp-etl-pipeline
This project is an automated ETL (Extract, Transform, Load) pipeline designed to extract, transfer, process, and schedule data workflows using Google Cloud Platform (GCP).

## Technologies Used
- **Python** (Requests, JSON)
- **Google Cloud Platform:**
  - Cloud Storage
  - BigQuery
  - Cloud Run Functions
  

## Project Workflow

## Setup and Installation
To run this project locally, you need to install the following libraries:

```bash
pip install google-cloud-storage google-cloud-bigquery requests

```
## Configuration
To connect the script to your Google Cloud account, ensure you have created the necessary resources in BigQuery and update the variables in the code:

- **Project ID:** `single-cycling-426112-e2`
- **Bucket Name:** `gcsproject` (Cloud Storage)
- **BigQuery Setup:**
  - **Dataset Name:** `cleandata` (Created to organize tables)
  - **Table Name:** `users_data` (Structured to receive processed JSON data)

  
## Data Lake Layering
I implemented a layering strategy to manage the data lifecycle effectively:

* **Landing Zone (Raw Layer):** - Saves the data in its original format: `row_data.json`.
    - **Why?** To preserve a "Single Source of Truth" and allow for re-processing without re-fetching from the API.
* **Processed Zone (Curated Layer):** - Saves the cleaned and transformed data: `clean_data.json`.
    - **Why?** To ensure the data is optimized, validated, and ready for analytical tools like **BigQuery**.

<img width="2860" height="1156" alt="image" src="https://github.com/user-attachments/assets/a0249244-a620-43d6-aa20-e3d305a484b9" />

## Results & Verification
After the pipeline execution, the data is successfully loaded into **BigQuery**. I verified the results by running SQL queries to ensure data integrity and accuracy.

### Sample SQL Query
You can query the processed data using the following SQL command:

```sql
SELECT 
    name,
    email,
    age,
    gender,
    country
FROM 
    `single-cycling-426112-e2.cleandata.users_data`
LIMIT 10;
```
<img width="2866" height="1562" alt="image" src="https://github.com/user-attachments/assets/2588e585-459c-4d88-bc41-9e02b2f032ee" />

<img width="2788" height="1042" alt="image" src="https://github.com/user-attachments/assets/036c30bd-640c-47be-9b75-6869bf53308f" />


## Deployment (Serverless Execution)
I deployed the ETL pipeline using **Google Cloud Run Functions** to ensure the process is scalable and can be triggered automatically.

- **Trigger Type:** HTTP / Cloud Scheduler
- **Runtime:** Python 3.x
- **Status:** Successfully deployed and executed.

### Execution Proof
When the function is triggered, it returns: 
`Pipeline Executed Successfully!`

> You can see the deployment metrics and successful request logs in the Google Cloud Console, confirming the pipeline is fully operational in a production-ready environment.
<img width="2854" height="884" alt="Screenshot 2026-05-12 013615" src="https://github.com/user-attachments/assets/2d50ac4e-32a2-4e2e-b6d6-bb0204fbc590" /> <img width="2870" height="1648" alt="Screenshot 2026-05-12 013658" src="https://github.com/user-attachments/assets/55b74601-78e6-48d3-b07a-17dee9ccbd6b" /> <img width="2880" height="724" alt="Screenshot 2026-05-12 013729" src="https://github.com/user-attachments/assets/675a83e7-9740-42d4-9aee-79cbc7641b04" />

## Data Flow Diagram
The following diagram illustrates how the data moves through the pipeline:

```text
[ API Source ] 
      |
      | (Fetch Data)
      v
[ Landing Zone (GCS) ]  --> File: row_data.json (Raw)
      |
      | (Clean & Transform)
      v
[ Processed Zone (GCS) ] --> File: clean_data.json (Clean)
      |
      | (Load Data)
      v
[ BigQuery Data Warehouse ] --> Table: users_data
      |
      | (Final Execution & Hosting)
      v
[ Cloud Run Functions ]

```

  
