# Agentic AI Research Assistant

An AI-powered research assistant that uses multiple specialized agents to answer questions by searching uploaded documents and the web, then synthesizing a unified response with source citations.

Built with LangGraph for agent orchestration, Ollama for local LLM inference, and ChromaDB for vector search — runs entirely on your machine with zero API costs.

## What It Does

You upload PDFs, ask a question, and the system figures out the best way to answer it:

- If your question is about the uploaded documents, it searches them using RAG
- If your question needs current information, it searches the web
- If it needs both, it calls both agents
- A synthesis agent then combines everything into a clear answer with citations

The coordinator agent uses an LLM to make routing decisions — it's not hardcoded rules, the model actually reads your question and decides which agents to call.

## Architecture
User Query
│
▼
Coordinator Agent (LLM-based routing)
│
├──► Document Agent ──► ChromaDB (vector search over PDFs)
│
├──► Web Search Agent ──► DuckDuckGo (real-time web results)
│
└──► Synthesis Agent ──► Ollama/Llama 3.2 (generates cited answer)
│
▼
Streamlit Chat UI (with agent visibility + source panel)
## Tech Stack

- **LangGraph** — StateGraph with conditional edges for agent orchestration
- **Ollama + Llama 3.2** — local LLM for routing decisions and answer generation
- **ChromaDB + sentence-transformers** — vector database for document retrieval
- **LangChain** — text splitting, Ollama integration
- **DuckDuckGo Search** — web search with no API key required
- **Streamlit** — chat interface with PDF upload and agent activity logs

## Key Features

**Multi-agent orchestration** — A coordinator agent analyzes each query and dynamically routes to the right combination of specialist agents using LLM-based planning, not keyword matching.

**Document Q&A with RAG** — Upload PDFs and ask questions. Documents are chunked (1000 chars, 200 overlap), embedded using sentence-transformers, and stored in ChromaDB for similarity retrieval.

**Real-time web search** — Queries that need current information are routed to DuckDuckGo. No API key needed.

**LLM synthesis with citations** — The synthesis agent receives context from all sources and generates a coherent answer, citing exactly which document page or web source each piece of information came from.

**Conversation memory** — Follow-up questions work naturally. Ask "What is a JOIN?" then "What about LEFT JOIN?" and it understands the context.

**Agent transparency** — Every response includes an expandable panel showing which agents were called, what they found, and the full source list. You can see the system's reasoning, not just the final answer.

**Fully local** — Everything runs on your machine using Ollama. No data leaves your system, no API costs.

**Error resilience** — Each agent is wrapped with error handling. If one agent fails (Ollama down, network issues), the others continue and the app stays running.

## Project Structure
agentic-research-assistant/
├── app.py                    # Streamlit chat interface
├── graph.py                  # LangGraph workflow with conditional routing
├── state.py                  # Shared state schema (AgentState)
├── agents/
│   ├── coordinator.py        # LLM-based query router
│   ├── document_agent.py     # RAG retrieval from ChromaDB
│   ├── web_agent.py          # DuckDuckGo web search
│   └── synthesis_agent.py    # LLM answer generation with citations
├── tools/
│   ├── rag_tool.py           # PDF extraction, chunking, embedding, search
│   └── search_tool.py        # DuckDuckGo search wrapper
├── utils/
│   └── error_handler.py      # Agent error handling wrapper
└── data/
└── documents/            # Uploaded PDFs
## Setup

### Prerequisites

- Python 3.10+
- Ollama installed ([ollama.com](https://ollama.com))

### Installation

```bash
git clone https://github.com/GirirajKudupudi/agentic-research-assistant.git
cd agentic-research-assistant

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Pull the LLM model

```bash
ollama pull llama3.2:1b
```

### Run

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start the app
streamlit run app.py
```

Open the browser, upload a PDF, and start asking questions.

## How the Graph Works

The core of this project is the LangGraph StateGraph defined in `graph.py`:

1. **State** — A shared `AgentState` dictionary flows through every node. Each agent reads what it needs and returns a partial update that LangGraph merges automatically.

2. **Conditional routing** — After the coordinator runs, a routing function checks the plan and directs execution to the right agents. This isn't a fixed pipeline — the path changes based on each query.

3. **Reducers** — The `agent_logs` field uses an append reducer (`Annotated[list[str], add]`) so every agent's logs accumulate instead of overwriting each other.
START → Coordinator → [Document Agent] → [Web Agent] → Synthesis → END
└──────────────────────────────────► Synthesis → END
└───────────────► [Web Agent] ─────► Synthesis → END
## What I Learned

- How LangGraph's StateGraph, conditional edges, and reducers work for agent orchestration
- Designing a multi-agent system where the coordinator uses an LLM to make routing decisions
- Building a RAG pipeline from scratch: PDF extraction, recursive chunking, vector embedding, similarity search
- Integrating local LLMs via Ollama for zero-cost, privacy-preserving inference
- Managing conversation memory across agent calls for natural follow-up questions
- Wrapping agents with error handling for production resilience