import os
from chromadb import PersistentClient
import ollama

# Path to the Chroma database
DB_DIR = os.path.expanduser("~/cyber-llm/rag/chroma")

# Load the persistent Chroma database
client = PersistentClient(path=DB_DIR)
collection = client.get_or_create_collection("cyber_notes")

def query_rag(q):
    """Query the vector database and send the retrieved context to the LLM."""
    results = collection.query(
        query_texts=[q],
        n_results=5
    )

    # Combine retrieved text chunks
    docs = results["documents"][0]
    context = "\n\n".join(docs)

    # Build the prompt for the LLM
    prompt = f"""
Use the context below to answer the question.

Context:
{context}

Question: {q}

Answer:
"""

    # Generate the response using Ollama
    response = ollama.generate(
        model="llama3",
        prompt=prompt
    )

    print("\n" + response["response"] + "\n")

if __name__ == "__main__":
    print("RAG ready. Ask anything from your notes.\n")
    while True:
        q = input("Ask: ")
        if q.strip().lower() in ["exit", "quit"]:
            break
        query_rag(q)
