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
- Kali Linux (VMware)
- Python
- Ollama (Llama 3)
- ChromaDB
- LangChain (light use for splitting and retrieval)
- Flask (optional web UI)

## Project Structure
project/
│── data/                # Raw notes and writeups  
│── processed/           # Cleaned and chunked text  
│── db/                  # Searchable database files  
│── app/  
│   ├── ingest.py        # Reads, cleans, chunks, and stores data  
│   ├── query.py         # Searches data and sends context to the LLM  
│   ├── utils.py         # Helper functions  
│── web/  
│   ├── app.py           # Simple Flask UI  
│   ├── templates/  
│── README.md  
│── SETUP.md             # Technical setup and commands  

## How It Works
The system loads your cybersecurity notes, breaks them into smaller readable sections, stores them in a searchable database, and uses a local LLM to answer questions based on the most relevant pieces of information. This creates a simple, offline‑capable assistant for reviewing and understanding security concepts.

## Documentation
For installation steps, commands, and a deeper technical breakdown, see:

SETUP.md
