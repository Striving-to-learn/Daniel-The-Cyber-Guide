# Daniel The Cyber Guide

Daniel (The Cyber Guide) is a local, offline AI assistant that lets you query your cybersecurity notes, HackTheBox / TryHackMe / CTF writeups, study material, and lab documentation using a local LLM (Llama 3 8B via Ollama).  
It uses a lightweight RAG-style pipeline: chunk all your notes, store them in ChromaDB, retrieve the relevant chunks, and inject them into the LLM prompt.

This gives you context-aware answers based on your own cybersecurity material, with everything running locally on Kali Linux.  
The goal: a fast, offline-capable assistant for learning and reviewing cybersecurity concepts.

Everything runs locally on Kali Linux. No internet required after setup.

Get started here: **[SETUP.md](SETUP.md)** For the  full installation, OS options, VM tools, and troubleshooting


## Quick Start

1. **Install Ollama and pull the model**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull llama3
   ```

2. **Create the project directory and add notes**
   ```bash
   mkdir -p ~/cyber-llm/{notes,rag,web}
   mkdir -p ~/cyber-llm/rag/chroma
   # Copy your markdown/.txt/.pdf notes into ~/cyber-llm/notes/
   ```

3. **Set up Python and install dependencies**
   ```bash
   cd ~/cyber-llm
   python3 -m venv venv
   source venv/bin/activate
   pip install chromadb langchain-text-splitters flask pypdf python-dotenv ollama
   ```

4. **Build the RAG database**
   ```bash
   python rag/build_rag.py
   ```

5. **Start querying**
   ```bash
   python rag/query_rag.py
   ```

👉 **For full installation steps, OS options, VM tools, FAQS and troubleshooting, see the detailed guide:**  
**[SETUP.md](SETUP.md)**


## Features
- Reads cybersecurity notes and lab writeups ( from Markdown, txt`, pdf files)  
- Breaks content into smaller chunks for easier searching  
- Stores information in a lightweight, persistent vector database (ChromaDB)  
- Runs a local LLM (Llama 3 8B via Ollama)  
- Provides context-aware answers using a simple retrieval workflow  
- Includes Python scripts for loading data (`build_rag.py`) and asking questions (`query_rag.py`)  
- Optional minimal web interface for querying the model (Flask)

## Tech Stack
- OS: Kali Linux (VMware or VirtualBox)  
  - Also works on Ubuntu, Debian, Pop!_OS, Parrot OS (Debian-based)
- Language: Python 3
- LLM Runtime: Ollama
- Model: Llama 3 (8B)
- Vector DB: ChromaDB (persistent)
- Text Splitters: LangChain text splitters
- Web UI (optional): Flask

## What This Is (and Isn’t)

This is a lightweight RAG-style pipeline: chunk your notes, embed them, store in ChromaDB, retrieve relevant chunks, and inject them into the LLM prompt. Knowledge lives in ChromaDB, not in the model.

This is not model training or fine-tuning. The LLM does not learn your notes, its weights never change, and when context is removed, that information is gone for that request.

Built for small-to-medium personal datasets (notes, labs, writeups), not enterprise. Retrieval quality depends on chunking and embeddings, and this is not a production-grade RAG system.

## Project Structure
```cyber-llm/
│── notes/             # Raw cybersecurity notes and writeups
│── rag/
│   ├── chroma/        # ChromaDB persistent database
│   ├── build_rag.py   # Ingests notes into ChromaDB
│   └── query_rag.py   # Queries ChromaDB and sends context to Ollama
│── web/
│   └── app.py        # Optional Flask UI
│── README.md
│── SETUP.md
```

