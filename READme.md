# GraphRAG Implementation with VertexAI

This project is a simple implementation of the Neo4j GraphRAG package using Google's LLM models in VertexAI.

## About the Dataset

This dataset is a sample of 100 rows extracted from Tomaz Bratanic's Arxiv paper [blog datasets](https://github.com/tomasonjo/blog-datasets).
It includes the following fields: paper id, summary, title, publish date and authors.

## Getting Started

### Obtain the Neo4j Credentials

Step 1: Sign Up for a Neo4j Account [here](https://console.neo4j.io/?product=aura-db&_gl=1*63th2s*_gcl_aw*R0NMLjE3MzI2MDg5ODUuQ2owS0NRaUFnSmE2QmhDT0FSSXNBTWlMN1Y5N0VEQURkbURaSnFZVENhdFJUMzl5ZXI3WS0wUExaOW5MWlhCSlVCb0ZmV1BEWG8zeTJLb2FBdXdWRUFMd193Y0I.*_gcl_au*MzI3MTk4NzkuMTcyNzgzMzE2Ng..*_ga*NjY4ODkyMzIuMTcxOTk4ODgxNg..*_ga_DL38Q8KGQC*MTczMzI3NzA0MC4zNy4xLjE3MzMyNzcwNTkuMC4wLjA.*_ga_DZP8Z65KK4*MTczMzI3NzA0MC40MC4xLjE3MzMyNzcwNTkuMC4wLjA.).

Step 2: Create a New Instance.

Step 3: Obtain the Neo4j credentials.txt file. Sample provided [here](https://github.com/justinsiowqi/graphrag/blob/main/Neo4j_credentials_sample.txt).

### Install Packages

```bash
pip install -r requirements.txt
```

### Ingest Dataset into Database

```bash
python ingest.py
```

### Create Embeddings and Retrieve Using GraphRAG

```bash
python main.py
```