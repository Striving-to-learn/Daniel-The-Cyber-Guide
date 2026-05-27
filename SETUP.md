# Technical Details

This project was built and tested inside a Kali Linux virtual machine running on VMware. The setup includes installing system packages, configuring a Python environment, installing Ollama for local LLM inference, and preparing a directory structure for storing cybersecurity notes and running the ingestion pipeline.

The system uses Python scripts to read notes, clean and split text, store them in a lightweight searchable database, and query them using a local LLM (Llama 3). All processing happens locally, and the assistant runs fully offline once installed.

---

# Operating System and Environment

**OS:** Kali Linux (VMware or VirtualBox)

The project was developed and tested on **Kali Linux**, but it should also work on other Debian‑based distributions such as **Ubuntu, Debian, Pop!_OS, and Parrot OS**. These systems share similar package managers and Python environments, so the installation steps are nearly identical.

Kali Linux was chosen because it includes many cybersecurity tools out of the box. Other distributions will work, but they may not include the same preinstalled security utilities.

Because Parrot OS and other Debian‑based distributions may package dependencies differently, some commands or package names may require small adjustments depending on the operating system version and installed repositories. Older or heavily modified Kali or Parrot installations may also require additional manual configuration due to outdated Python layers or older package versions.

## System Updates

```bash
sudo apt update && sudo apt full-upgrade -y
```

## VMware Tools

If using VMware, install the VMware guest tools for better display scaling, clipboard sharing, and VM integration.

```bash
sudo apt install -y open-vm-tools open-vm-tools-desktop
```

This project was personally built and tested using VMware.

## VirtualBox Guest Additions

If using VirtualBox, install the VirtualBox guest additions for improved VM support and desktop integration.

```bash
sudo apt install -y virtualbox-guest-x11 virtualbox-guest-utils virtualbox-guest-dkms
```

## Choosing the Correct OS Image

You can install Kali Linux or Parrot OS (Security Edition) using either a standard ISO or a prebuilt virtual machine image. Prebuilt images are generally faster and easier to configure because many settings and drivers are already prepared.

### Kali Linux Images
Kali Linux images can be downloaded from:

https://www.kali.org/get-kali/#kali-platforms

You can choose between:

Installer Images — traditional ISO files used for manual installation

Virtual Machines — prebuilt VMware and VirtualBox images

If you want a standard ISO installer, select the Installer Images section.

If you want a preconfigured virtual machine, select the Virtual Machines section and download either the VMware or VirtualBox image.

Prebuilt VM images are typically the fastest option because they include optimized drivers and preconfigured settings.

### Parrot OS (Security Edition) Images
Parrot OS Security Edition can be downloaded from:

https://parrotsec.org/download/

Available formats include:

ISO — for bare metal, laptops, desktops, or manual VM installation

OVA — optimized for VirtualBox

VMDK — optimized for VMware

The Parrot Security Edition includes penetration testing tools similar to Kali and is fully compatible with this project. Installation steps are nearly identical to Kali because Parrot is also Debian‑based. 
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

A dedicated directory was created to store notes, scripts, databases, and model-related files.

## Create the Directories

```bash
mkdir -p ~/cyber-llm/{notes,rag,training,models}
mkdir -p ~/cyber-llm/notes/{obsidian,hacktricks,blue-team,red-team,resources}
```

Cybersecurity notes, Obsidian vaults, and lab writeups should be copied into:

```bash
~/cyber-llm/notes/
```

This directory acts as the primary data source for ingestion.

## Common Directory Issues

One common issue is attempting to access directories before they exist.

Example:

```bash
ls -l ~/cyber-llm/rag
```

Possible error:

```text
No such file or directory
```

This usually means the directory structure was not created yet. Re-run the `mkdir -p` commands shown earlier.

Another common issue involves copying note directories from incorrect or non-existent paths.

Example:

```bash
cp -r "/path/to/notes" ~/cyber-llm/notes/obsidian/
```

Possible error:

```text
cannot stat '/path/to/notes': No such file or directory
```

This indicates the source directory path is incorrect or does not exist. Verify the source path before copying files.

---

# Python Environment

A Python virtual environment was created to isolate dependencies and avoid conflicts with Kali Linux system packages.

## Why a Virtual Environment Is Required

Kali Linux follows PEP 668 restrictions, which prevent many system-wide `pip` installations. Because of this, packages such as ChromaDB must be installed inside a Python virtual environment.

This is expected behavior on modern Kali Linux systems.

## Create and Activate the Virtual Environment

```bash
python3 -m venv ~/cyber-llm/venv
source ~/cyber-llm/venv/bin/activate
```

When activated, the shell prompt should change to something similar to:

```text
(venv) kali@kali:~
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

## Common Python Dependency Errors

### ChromaDB Not Installed

Example:

```bash
python3 ~/cyber-llm/rag/build_rag.py
```

Possible error:

```text
ModuleNotFoundError: No module named 'chromadb'
```

This usually means the script was executed outside the virtual environment.

Activate the virtual environment first:

```bash
source ~/cyber-llm/venv/bin/activate
```

Then install dependencies:

```bash
pip install chromadb
```

### Missing langchain_text_splitters Module

Possible error:

```text
ModuleNotFoundError: No module named 'langchain_text_splitters'
```

Fix by installing the package:

```bash
pip install langchain-text-splitters
```

---

# ChromaDB Compatibility Notes

Recent ChromaDB releases introduced breaking API changes.

Older tutorials may use deprecated client syntax such as:

```python
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=DB_DIR
))
```

Newer ChromaDB versions use the updated API:

```python
from chromadb import PersistentClient

client = PersistentClient(path=DB_DIR)
collection = client.get_or_create_collection("cyber_notes")
```

If you encounter errors related to deprecated Chroma configuration, update the ingestion script to use the newer API.

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

If using a separate RAG build script:

```bash
python ~/cyber-llm/rag/build_rag.py
```

This generates the database inside:

```bash
project/db/
```

A successful run should end with output similar to:

```text
Ingestion complete.
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

# Hardware Considerations

This project does not require high-end hardware, but performance improves with additional memory.

- Minimum recommended RAM: **8 GB**
- Recommended RAM for smoother performance: **16 GB**
- CPU: Any modern multi-core processor
- Disk space: Approximately **10–15 GB** for Kali, notes, dependencies, and model storage

Ollama and Llama 3 will run on systems with 8 GB RAM, but ingestion speed and model response times improve significantly with more memory.

---

# Notes Backup and Format Recommendations

If you are ingesting personal notes (Obsidian vaults, Notion exports, OneNote pages, etc.), back them up before running the ingestion pipeline.

The ingestion process does not modify the original files, but maintaining backups helps prevent accidental data loss or corruption.

## Recommended Formats

- Markdown (`.md`) — preferred format
- Plain text (`.txt`)
- PDF (`.pdf`) — supported, but parsing quality may vary

## Exporting From Other Platforms

### Obsidian

Obsidian already uses Markdown format.

### Notion

Export notes using the **Markdown & CSV** option.

### OneNote

Export as PDF or manually convert notes to Markdown.

---

# Summary of Tools Used

| Tool | Purpose |
|---|---|
| Kali Linux | Development environment |
| Python 3 | Scripting and backend logic |
| Ollama | Local LLM runtime |
| Llama 3 | Model used for answering questions |
| ChromaDB | Lightweight searchable vector database |
| LangChain | Text splitting and retrieval helpers |
| Flask | Optional web interface |
| VMware / VirtualBox | Virtualization platform |
