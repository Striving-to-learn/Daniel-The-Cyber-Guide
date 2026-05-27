import os
from chromadb import PersistentClient
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Paths for notes and the Chroma database
NOTES_DIR = os.path.expanduser("~/cyber-llm/notes")
DB_DIR = os.path.expanduser("~/cyber-llm/rag/chroma")

# Initialize or load the persistent Chroma database
client = PersistentClient(path=DB_DIR)
collection = client.get_or_create_collection("cyber_notes")

# Split markdown files into manageable chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=["\n\n", "\n", " ", ""]
)

def load_markdown_files():
    """Recursively collect all markdown files from the notes directory."""
    md_files = []
    for root, _, files in os.walk(NOTES_DIR):
        for f in files:
            if f.endswith(".md"):
                md_files.append(os.path.join(root, f))
    return md_files

def ingest():
    """Read markdown files, split them into chunks, and store them in ChromaDB."""
    md_files = load_markdown_files()
    print(f"Found {len(md_files)} markdown files to ingest.")

    for path in md_files:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = splitter.split_text(text)

        for i, chunk in enumerate(chunks):
            doc_id = f"{os.path.basename(path)}-{i}"
            collection.add(
                documents=[chunk],
                ids=[doc_id],
                metadatas=[{"source": path}]
            )

        print(f"Ingested: {path}")

    print("Ingestion complete.")

if __name__ == "__main__":
    ingest()
