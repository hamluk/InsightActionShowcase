# Insight Action Showcase

The **Insight Action Showcase** demonstrates an end-to-end AI workflow that turns unstructured documents into **actionable business decisions**.

The system covers the full pipeline from **document ingestion** to **human-approved execution**:

**Documents → Insights → Actions → Approval → Execution**

This repository is intended as a **technical showcase** for AI-powered decision support systems, not as a finished product.

---

## What this Showcase Demonstrates

- Retrieval-Augmented Generation (RAG) on uploaded documents  
- Structured insight extraction with source traceability  
- Automated action proposal generation  
- Human-in-the-loop approval flow  
- Explicit separation between AI reasoning and human decision-making  

---

## Core Features

### Document Ingestion & Vector Storage
Documents can be uploaded and embedded into a vector database.  
All insights and actions are derived **exclusively** from these indexed documents.

### Document Overview
The UI provides a clear overview of all uploaded and indexed files, ensuring transparency about the system’s knowledge base.

### Configurable System Prompts
Two independent system prompts are exposed and editable:
- **Insight Prompt** – controls how insights are extracted
- **Action Prompt** – controls how actions are derived from insights

This allows controlled experimentation without code changes.

### Document-Based Questioning
Users can ask questions that are answered strictly based on the uploaded documents using RAG.

### Insight Generation with Source References
Insights are presented in a summarized form.
Each insight includes expandable details with **exact page references** from the source documents.

### Action Proposals from Insights
Each insight can be transformed into a structured **Action Proposal**, describing concrete next steps derived from the extracted information.

### Approval Flow & Execution
Actions must be explicitly approved by a human.
Once approved, an **automated email is sent** containing all relevant action details, demonstrating a real execution step.

---

## Architecture Overview

- **UI**: Streamlit  
- **LLM Orchestration**: LangChain  
- **Vector Store**: Qdrant  
- **Models**: OpenAI-compatible chat and embedding models  
- **Execution Example**: SMTP-based email sending  

The architecture is intentionally modular and production-oriented.

---

## Tech Stack

- Python 3.13
- Streamlit
- LangChain (Core, Community, OpenAI, Qdrant)
- Qdrant Vector Database
- Pydantic Settings
- Ruff (Linting & Formatting)

---

## Purpose of This Repository

This project is designed to:
- Demonstrate realistic AI agent workflows
- Show how AI can support, not replace, human decisions
- Serve as a discussion and demo artifact for clients and stakeholders
- Provide a clean reference architecture for Insight → Action systems

---

## Disclaimer

This is a **showcase project**.  
Security, scaling, authentication, and production hardening are intentionally simplified.

---

## Author

Lukas Hamm

🔗 [https://www.lukashamm.dev](https://lukashamm.dev)  
📧 [lukas@lukashamm.dev](lukas@lukashamm.dev)  
💼 [https://www.linkedin.com/in/lukashamm-dev](https://www.linkedin.com/in/lukashamm-dev)
