from langchain_community.graphs import Neo4jGraph

# Insert Neo4j Credentials + Details Here
credentials_file_path = "Neo4j_credentials_sample.txt"

# Instantiate connection to Neo4j
def read_credentials(file_path):
    credentials = {}
    with open(file_path, 'r') as f:
        for line in f:
            # Skip comment lines
            if line.startswith("#") or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            credentials[key] = value
    return credentials

# Read the credentials from the file
creds = read_credentials(credentials_file_path)

# Extracting credentials
NEO4J_URI = creds.get("NEO4J_URI")
NEO4J_USERNAME = creds.get("NEO4J_USERNAME")
NEO4J_PASSWORD = creds.get("NEO4J_PASSWORD")

# Connect to Neo4j Graph Database
graph = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
)

# Import Arxiv information
arxiv_query = """
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/justinsiowqi/graphrag/main/arxiv_small.csv' AS row
WITH row
MERGE (p:Paper {id: row.paper_id})  
SET p.title = row.title, p.summary = row.summary, p.date = row.publish_date 
MERGE (a:Authors {authors: row.authors})  
MERGE (a)-[:WROTE]->(p) 
"""

graph.query(arxiv_query)