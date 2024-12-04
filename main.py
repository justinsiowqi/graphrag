from neo4j import GraphDatabase
from neo4j_graphrag.retrievers import VectorRetriever
from neo4j_graphrag.llm import VertexAILLM
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.embeddings.vertexai import VertexAIEmbeddings
from neo4j import GraphDatabase
from neo4j_graphrag.indexes import create_vector_index, drop_index_if_exists
from vertexai.language_models import TextEmbeddingModel

# Insert Path to the credentials file
credentials_file_path = "Neo4j_credentials_sample.txt"
INDEX_NAME = "chunk-index"
DIMENSION=768 #Google Text Embedding 004 Dimensions

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

# Connect to Neo4j database
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

# Initialize the Embedding Model
embedder = VertexAIEmbeddings("text-embedding-004")

# Delete all Nodes and Relationships
with driver.session() as session:
    result = session.run("MATCH (n) DETACH DELETE n")

# Drop Existing Index
drop_index_if_exists(driver, INDEX_NAME)

# Function to get embeddings from OpenAI's API
def get_embedding(text):
    embedding = embedder.embed_query(text)
    return embedding

# Function to update the embeddings in Neo4j
def create_embeddings_for_papers():
    with driver.session() as session:
        
        # Filter Out Paper Without Summaries
        result = session.run("MATCH (p:Paper) WHERE p.summary IS NOT NULL RETURN p.id AS id, p.summary AS summary")

        for record in result:
            paper_id = record["id"]
            summary = record["summary"]

            embedding = get_embedding(summary)

            # Store the Embedding in the Paper Node
            session.run(
                "MATCH (p:Paper {id: $id}) "
                "SET p.summary_embedding = $embedding",
                id=paper_id,
                embedding=embedding
            )
            print(f"Created embedding for Paper ID: {paper_id}")

# Run the function to create embeddings
create_embeddings_for_papers()

# Creating the index
create_vector_index(
    driver,
    INDEX_NAME,
    label="Paper",
    embedding_property="summary_embedding",
    dimensions=DIMENSION,
    similarity_fn="euclidean",
)

# Initialize the retriever
retriever = VectorRetriever(driver, INDEX_NAME, embedder)

# 3. LLM
llm = VertexAILLM(
    model_name="gemini-1.5-flash-002"
)

# Initialize the RAG pipeline
rag = GraphRAG(retriever=retriever, llm=llm)

if __name__ == "__main__":
    # Query the graph
    query_text = "Tell me more about GraphRNN?"
    response = rag.search(query_text=query_text, retriever_config={"top_k": 5})
    print(response.answer)