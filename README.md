# Daniel — The Cyber Guide

Daniel (The Cyber Guide) is a local, offline AI assistant that lets you query your cybersecurity notes, HackTheBox / TryHackMe / CTF writeups, study material, and lab documentation using a local LLM (**Llama 3 8B** via Ollama).

It uses a lightweight RAG-style pipeline: chunk all your notes, **embed them into vectors**, store them in ChromaDB, retrieve relevant chunks using **vector similarity**, and inject them into the LLM prompt. This gives you context-aware answers based on your own cybersecurity material, with everything running locally on Kali Linux.

The goal: a fast, offline-capable assistant for learning and reviewing cybersecurity concepts.

**Purpose:** Provide cybersecurity guidance, teach better penetration testing skills, and help analyze prior engagements/labs. Everything runs locally on Kali Linux. No internet required after setup.

 **Get started here:** **[SETUP.md](SETUP.md)** *(Full installation, OS options, VM tools, FAQs, and troubleshooting)*

---

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
   # Copy your Markdown/.txt/.pdf notes into ~/cyber-llm/notes/
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

 **For full installation steps, OS options, VM tools, FAQs, and troubleshooting, see the detailed guide:**  
**[SETUP.md](SETUP.md)**

---

## What This Is (and Isn't)

This is a **lightweight RAG-style pipeline**: chunk your notes, embed them into vectors, store in ChromaDB, retrieve relevant chunks using vector similarity, and inject them into the LLM prompt. Knowledge lives in **ChromaDB**, not in the model.

This is **not** model training or fine-tuning. The LLM does **not learn** your notes, its weights never change, and when context is removed, that information is gone for that request.

Built for **small-to-medium personal datasets** (notes, labs, writeups), not enterprise. Retrieval quality depends on chunking and embeddings, and this is not a production-grade RAG system.

For a more production-grade cybersecurity RAG architecture:  
- https://github.com/simeononsecurity/sos-cyber-rag

---

## Features

- Reads cybersecurity notes and lab writeups (from Markdown, `.txt`, `.pdf` files)  
- Breaks content into smaller chunks for easier searching  
- Stores information in a lightweight, persistent **vector database** (ChromaDB)  
- Runs a local LLM (**Llama 3 8B** via Ollama)  
- Provides context-aware answers using a simple retrieval workflow  
- Includes Python scripts for loading data (`build_rag.py`) and asking questions (`query_rag.py`)  
- Optional minimal web interface for querying the model (Flask)

---

## Tech Stack

- OS: Kali Linux (VMware or VirtualBox)  
  - Also technically works on Ubuntu, Debian, Pop!_OS, Parrot OS (Debian-based), but has not been tested by the developer yet
- **Language:** Python 3
- **LLM Runtime:** Ollama
- **Model:** Llama 3 **(8B)**
- **Vector DB:** ChromaDB (persistent, with embeddings)
- **Text Splitters:** LangChain text splitters
- **Web UI (optional):** Flask

---

## Project Structure

```text
cyber-llm/
│── notes/             # Raw cybersecurity notes and writeups
│── rag/
│   ├── chroma/        # ChromaDB persistent database
│   ├── build_rag.py   # Ingests notes into ChromaDB
│   └── query_rag.py   # Queries ChromaDB and sends context to Ollama
│── web/
│   └── app.py         # Optional Flask UI
│── README.md
│── SETUP.md
```

---

## Common Use Cases

**Most common use case:** After completing TryHackMe or HackTheBox machines, query your writeups to review techniques, tools, and concepts for future penetration testing engagements.

Example questions:

```text
How did I solve the TryHackMe 'Jr Penetration Tester' path machines?
What was the vulnerability in the HTB 'Lame' machine?
How do I perform Kerberoasting again?
What tools did I use for credential dumping in my last lab?
How do I detect lateral movement from my notes?
```

---

## Legal and Ethical Notice

**Important:** This project was developed using **my personal cybersecurity notes** (TryHackMe writeups, HackTheBox labs, personal study material) in my own home lab environment. I only used these notes because they are **my own** — created through my own learning and work.

**DO NOT:**
- Steal proprietary data from companies
- Use copyrighted material you don't own
- Ingest confidential business information without permission
- Publish or share someone else's proprietary notes

**This project is for personal use only.** Your notes are stored locally in ChromaDB and never leave your system. However, you should only ingest data you own or have permission to use.

**Important Clarification:** My personal notes **will never appear in this public GitHub repository**. They are **only available on my own machine** and are **not disclosed anywhere** in this documentation. This means:
- No laws are being broken
- No proprietary writeups are being shared
- No copyrighted material is exposed
- This is purely a technical setup guide, not a content repository

> **Note:** This guide only covers installation and technical setup. Your data stays 100% local and private.

---

## Data Privacy and Production Use

**Important:** This project can be applied to other fields where data privacy is critical:
- **Healthcare** (HIPAA-compliant patient data)
- **Finance** (sensitive financial records)
- **Government** (classified or confidential data)
- **Enterprise** (proprietary business information)

**The secure part:** None of this data leaves the machine — it stays 100% local in ChromaDB.

**Production warning:** If you use this in production, you must **harden the machine from external attacks** (firewall, network isolation, access controls, encryption). This project is not production-ready by default.

---

## Disclaimer

**I take no responsibility for any of your private data you train on this.** That is **your responsibility**.

You are responsible for:
- Ensuring you have permission to use the data you ingest
- Backing up your notes before ingestion
- Securing your machine if used in production
- Compliance with relevant laws (HIPAA, GDPR, etc.) if using sensitive data

This is a **personal learning project**, not enterprise software. Use it responsibly.

---

## Future Project Phases

This is a version 1 personal project with potential future enhancements:

**Planned phases:**
1. **Open-source data integration** — Add publicly available cybersecurity resources (documentation, guides, open writeups) during ingestion
2. **Model research** — Test alternative models (Mistral, Phi, Gemma) that might perform better for cybersecurity queries
3. **Cross-platform testing** — Further testing on alternative platforms like Pop!_OS, Ubuntu, Debian, Parrot OS, VirtualBox, etc. to ensure compatibility
4. **Better embeddings** — Implement custom embedding models optimized for technical/security content
5. **Reranking** — Add hybrid search (vector + keyword) and reranking for improved retrieval quality
6. **Web UI improvements** — Add authentication, multi-user support, and better interface

These are **not implemented yet**. This version is designed for small-to-medium personal datasets only.
