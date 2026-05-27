# Daniel-The-Cyber-Guide

Daniel the Cyber Guide is a local AI assistant that reads cybersecurity notes, HackTheBox writeups, TryHackMe material, and personal lab documentation. It organizes the information so a local LLM can answer security questions with relevant context. The project was built in a Kali Linux home lab using Python, Ollama, and a small text‑search database.

The goal is to create a fast, offline‑friendly assistant for learning and reviewing cybersecurity topics.

## Features
- Reads cybersecurity notes and lab writeups  
- Breaks content into smaller pieces for easier searching  
- Stores information in a lightweight searchable database  
- Runs a local LLM (Llama 3 via Ollama)  
- Provides context‑aware answers using a simple retrieval workflow  
- Includes Python scripts for loading data and asking questions  
- Optional minimal web interface for querying the model  

## Tech Stack
- Kali Linux (VMware or VirtualBox)
- Python 3
- Ollama
- Llama 3
- ChromaDB
- LangChain text splitters
- Flask (optional web UI)

## Project Structure
cyber-llm/
│── notes/             # Raw cybersecurity notes and writeups
│── rag/
│   ├── chroma/        # ChromaDB persistent database
│   ├── build_rag.py   # Ingests notes into ChromaDB
│   └── query_rag.py   # Queries ChromaDB and sends context to Ollama
│── web/
│   └── app.py        # Optional Flask UI
│── README.md
│── SETUP.md

## How It Works
The system loads your cybersecurity notes, breaks them into smaller readable sections, stores them in a searchable database, and uses a local LLM to answer questions based on the most relevant pieces of information. This creates a simple, offline‑capable assistant for reviewing and understanding security concepts.

## Documentation
For installation steps, commands, and technical details, see SETUP.md.
