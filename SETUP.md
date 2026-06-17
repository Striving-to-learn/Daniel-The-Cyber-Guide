# SETUP.md — Full Installation & Technical Details

This guide covers everything you need to install and run **Daniel — The Cyber Guide** inside a Kali Linux virtual machine. It includes system updates, VM tools, Ollama setup, Python environment configuration, directory structure, ingestion, querying, and common troubleshooting.

All processing happens **locally**, and the assistant runs **fully offline** once installed.

---

## Quick Overview

1. Update Kali Linux and install VM tools  
2. Install Ollama and pull **Llama 3 8B**  
3. Create the project directory structure  
4. Set up a Python virtual environment  
5. Install Python dependencies  
6. Copy your notes into `~/cyber-llm/notes/`  
7. Run the ingestion script (`build_rag.py`)  
8. Run the query script (`query_rag.py`)  

For a shorter version, see the **Quick Start** section in `README.md`.

---

## Operating System and Environment

**OS:** Kali Linux (VMware or VirtualBox)

This project was developed and tested on **Kali Linux**, but it should also work on other Debian-based distributions:

- Ubuntu
- Debian
- Pop!_OS
- Parrot OS (Security Edition)

These systems share similar package managers and Python environments, so the installation steps are nearly identical.

Kali Linux was chosen because it includes many cybersecurity tools out of the box. Other distributions will also work, but they may not include the same preinstalled security utilities and might require additional installation steps and configuration.

---

## System Updates

Always start with a fresh and updated system:

```bash
sudo apt update && sudo apt full-upgrade -y
```

---

## VMware Tools

If using VMware, install the VMware guest tools for better display scaling, clipboard sharing, and VM integration:

```bash
sudo apt install -y open-vm-tools open-vm-tools-desktop
```

This project was personally built and tested using VMware.

---

## VirtualBox Guest Additions

If using VirtualBox, install the VirtualBox guest additions for improved VM support and desktop integration:

```bash
sudo apt install -y virtualbox-guest-x11 virtualbox-guest-utils virtualbox-guest-dkms
```

---

## Choosing the Correct OS Image

You can install Kali Linux or Parrot OS (Security Edition) using either a standard ISO or a prebuilt virtual machine image. Prebuilt images are generally faster and easier to configure because many settings and drivers are already prepared.

### Kali Linux Images

Download from: https://www.kali.org/get-kali/#kali-platforms

Available options:

- **Installer Images** — traditional ISO files for manual installation
- **Virtual Machines** — prebuilt VMware and VirtualBox images

For a standard ISO installer: select **Installer Images**.  
For a preconfigured VM: select **Virtual Machines** and download either VMware or VirtualBox image.

Prebuilt VM images are typically the fastest option because they include optimized drivers and preconfigured settings.

### Parrot OS (Security Edition) Images

Download from: https://parrotsec.org/download/

Available formats:

- **ISO** — for bare metal, laptops, desktops, or manual VM installation
- **OVA** — optimized for VirtualBox
- **VMDK** — optimized for VMware

Parrot Security Edition includes penetration testing tools similar to Kali and is fully compatible with this project.

---

## Local LLM Runtime (Ollama)

Ollama is used to run Llama 3 locally.

### Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Download the Model

```bash
ollama pull llama3
```

> This pulls **Llama 3 8B**, which is designed to be practical on home lab hardware.

### Test the Model

```bash
ollama run llama3 "Hello from my Kali VM."
```

If you get a response, Ollama is working correctly.

---

## Project Directory Structure

Create the main folders:

```bash
mkdir -p ~/cyber-llm/{notes,rag,web}
mkdir -p ~/cyber-llm/rag/chroma
```

Copy your markdown notes, lab writeups, and cybersecurity material into:

```bash
~/cyber-llm/notes/
```

This directory acts as the primary data source for ingestion.

### Common Directory Issues

#### Directory Doesn't Exist

```bash
ls -l ~/cyber-llm/rag
```

**Error:**
```text
No such file or directory
```

**Fix:** Re-run the `mkdir -p` commands:
```bash
mkdir -p ~/cyber-llm/{notes,rag,web}
mkdir -p ~/cyber-llm/rag/chroma
```

#### Copying from Wrong Path

```bash
cp -r "/path/to/notes" ~/cyber-llm/notes/obsidian/
```

**Error:**
```text
cannot stat '/path/to/notes': No such file or directory
```

**Fix:** Verify the source path exists before copying:
```bash
ls "/path/to/notes"
```

---

## Python Environment

A Python virtual environment isolates dependencies and avoids conflicts with Kali Linux system packages.

### Why a Virtual Environment Is Required

Kali Linux follows **PEP 668** restrictions, which prevent many system-wide `pip` installations. Packages like ChromaDB must be installed inside a Python virtual environment.

This is expected behavior on modern Kali Linux systems.

### Create and Activate the Virtual Environment

```bash
python3 -m venv ~/cyber-llm/venv
source ~/cyber-llm/venv/bin/activate
```

When activated, the shell prompt should change to:

```text
(venv) kali@kali:~
```

### Install Required Packages

```bash
pip install chromadb langchain-text-splitters flask pypdf python-dotenv ollama
```

These packages support:

- Text cleaning and splitting
- Storing searchable text chunks
- Running the ingestion and query scripts
- Optional web interface

### Common Python Dependency Errors

#### ChromaDB Not Installed

```bash
python3 ~/cyber-llm/rag/build_rag.py
```

**Error:**
```text
ModuleNotFoundError: No module named 'chromadb'
```

**Fix:** This usually means the script was executed outside the virtual environment.

Activate the virtual environment first:
```bash
source ~/cyber-llm/venv/bin/activate
```

Then install dependencies:
```bash
pip install chromadb
```

#### Missing langchain_text_splitters Module

**Error:**
```text
ModuleNotFoundError: No module named 'langchain_text_splitters'
```

**Fix:**
```bash
pip install langchain-text-splitters
```

---

## ChromaDB Compatibility Notes

Recent ChromaDB releases introduced breaking API changes.

Older tutorials may use deprecated client syntax:

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

Make sure both `build_rag.py` and `query_rag.py`:

- Use `PersistentClient`
- Use `get_or_create_collection()` or `get_collection()` consistently
- Use the collection name `"cyber_notes"` in both scripts

If you see errors related to deprecated Chroma configuration, update your ingestion script to use the newer API.

---

## Ingestion Pipeline

The ingestion script (`build_rag.py`):

- Reads raw markdown notes from `~/cyber-llm/notes/`
- Cleans and normalizes text
- Splits text into smaller chunks
- **Embeds chunks into vectors** and stores them in ChromaDB

### Run the Ingestion

```bash
cd ~/cyber-llm
source venv/bin/activate
python rag/build_rag.py
```

This generates the ChromaDB database in:

```bash
~/cyber-llm/rag/chroma/
```

A successful run ends with:

```text
Ingestion complete.
```

---

## Query Pipeline

The query script (`query_rag.py`):

- Loads the ChromaDB database from `~/cyber-llm/rag/chroma/`
- **Embeds your query** into a vector
- **Retrieves the most similar chunks** using vector similarity
- Sends them to Llama 3 via Ollama
- Prints a context-aware answer

### Run the Query Script (Interactive)

```bash
cd ~/cyber-llm
source venv/bin/activate
python rag/query_rag.py
```

You will see:

```text
RAG ready. Ask anything from your notes.

Ask:
```

**Most common use case questions:**

```text
How did I solve the TryHackMe 'Jr Penetration Tester' path machines?
What was the vulnerability in the HTB 'Lame' machine?
How do I perform Kerberoasting again?
What tools did I use for credential dumping in my last lab?
How do I detect lateral movement from my notes?
```

**Other example questions:**

```text
Explain Kerberoasting
What is credential dumping?
How do I detect lateral movement?
```

---

## Optional Web UI

### Start the Web Interface

Ensure you're in the project root and the virtual environment is active:

```bash
cd ~/cyber-llm
source venv/bin/activate
python web/app.py
```

Open in your browser:

```text
http://localhost:5000
```

---

## Hardware Considerations

This project does not require high-end hardware, but performance improves with additional memory:

- **Minimum recommended RAM:** 8 GB
- **Recommended RAM for smoother performance:** 16 GB
- **CPU:** Any modern multi-core processor
- **Disk:** Approximately 10–15 GB for Kali, notes, dependencies, and model storage

**Llama 3 8B** will run on 8 GB RAM, but ingestion speed and model response times improve significantly with more memory.

---

## Notes Backup and Format Recommendations

Before ingesting personal notes:

- **Back up your notes** (Obsidian vaults, Notion exports, OneNote pages, etc.)
- The ingestion process does **not** modify original files, but backups prevent accidental data loss.

### Recommended Formats

- Markdown (`.md`) — preferred
- Plain text (`.txt`)
- PDF (`.pdf`) — supported, but parsing quality may vary

### Exporting From Other Platforms

- **Obsidian:** Already Markdown
- **Notion:** Export as **Markdown & CSV**
- **OneNote:** Export as PDF or convert to Markdown manually

---

## Summary of Tools Used

| Tool          | Purpose                                 |
|---------------|-----------------------------------------|
| Kali Linux    | Development environment                 |
| Python 3      | Scripting and backend logic             |
| Ollama        | Local LLM runtime                       |
| Llama 3 8B    | Model used for answering questions      |
| ChromaDB      | Lightweight searchable vector database  |
| LangChain     | Text splitting and retrieval helpers    |
| Flask         | Optional web interface                  |
| VMware / VB   | Virtualization platform                 |
