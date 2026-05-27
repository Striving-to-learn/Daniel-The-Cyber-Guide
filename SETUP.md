# Technical Details

This project was built and tested inside a Kali Linux virtual machine running on VMware. The setup includes installing system packages, configuring a Python environment, installing Ollama for local LLM inference, and preparing a directory structure for storing cybersecurity notes and running the ingestion pipeline.

The system uses Python scripts to read notes, clean and split text, store it in a lightweight searchable database, and query it using a local LLM (Llama 3). All processing happens locally, and the assistant runs fully offline once installed.

---

# Operating System and Environment

**OS:** Kali Linux (VMware guest)

## System Updates

```bash
sudo apt update && sudo apt full-upgrade -y
```

## VMware Tools

```bash
sudo apt install -y open-vm-tools open-vm-tools-desktop
```

---

# Local LLM Runtime (Ollama)

Ollama is used to run Llama 3 locally.

## Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## Download the Model

```bash
ollama pull llama3
```

## Test the Model

```bash
ollama run llama3 "Hello from my Kali VM."
```

This confirms that the local LLM runtime is working correctly.

---

# Project Directory Structure

A dedicated directory was created to store notes, scripts, and model-related files.

## Create the Directories

```bash
mkdir -p ~/cyber-llm/{notes,rag,training,models}
mkdir -p ~/cyber-llm/notes/{obsidian,hacktricks,blue-team,red-team,resources}
```

Cybersecurity notes, Obsidian vaults, and lab writeups should be copied into:

```bash
~/cyber-llm/notes/
```

This directory acts as the data source for ingestion.

---

# Python Environment

A virtual environment was created to isolate dependencies.

## Create and Activate the Virtual Environment

```bash
python3 -m venv ~/cyber-llm/venv
source ~/cyber-llm/venv/bin/activate
```

## Install Required Packages

```bash
pip install chromadb langchain langchain-text-splitters flask pypdf python-dotenv
```

These packages support:

- Text cleaning and splitting
- Storing searchable text chunks
- Running the ingestion and query scripts
- Optional web interface

---

# Ingestion Pipeline

The ingestion script performs the following steps:

- Reads raw notes from `data/`
- Cleans and normalizes text
- Splits text into smaller sections
- Stores sections in a searchable database (ChromaDB)

## Run the Ingestion

```bash
python app/ingest.py
```

This generates the database inside:

```bash
project/db/
```

---

# Query Pipeline

The query script:

- Searches the stored text
- Retrieves the most relevant sections
- Sends them to Llama 3 via Ollama
- Prints a context-aware answer

## Example Query

```bash
python app/query.py "Explain Kerberoasting"
```

---

# Optional Web Interface

A simple Flask UI is included for browser-based queries.

## Start the Web Interface

```bash
python web/app.py
```

Open in your browser:

```text
http://localhost:5000
```

---

# Summary of Tools Used

| Tool | Purpose |
|---|---|
| Kali Linux | Development environment |
| Python 3 | Scripting and backend logic |
| Ollama | Local LLM runtime |
| Llama 3 | Model used for answering questions |
| ChromaDB | Lightweight text search database |
| LangChain | Text splitting and retrieval helpers |
| Flask | Optional web interface |
