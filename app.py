"""
Streamlit UI for the Agentic Research Assistant.
Chat interface with PDF upload and agent visibility.
"""

import streamlit as st
import os
from graph import build_graph
from tools.rag_tool import index_pdf, get_chroma_collection

# Page config
st.set_page_config(
    page_title="Agentic Research Assistant",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 Agentic Research Assistant")
st.caption("Multi-agent system: Document RAG + Web Search + LLM Synthesis")


# --- Sidebar: PDF Upload ---
with st.sidebar:
    st.header("📄 Upload Documents")

    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file:
        # Save to data/documents/
        save_path = os.path.join("data", "documents", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Index into ChromaDB
        with st.spinner(f"Indexing {uploaded_file.name}..."):
            num_chunks = index_pdf(save_path)
            st.success(f"Indexed {num_chunks} chunks from {uploaded_file.name}")

    # Show indexed documents
    st.divider()
    st.subheader("Indexed Documents")
    collection = get_chroma_collection()
    count = collection.count()

    if count > 0:
        st.write(f"📊 {count} chunks in database")
        # List unique document names
        all_docs = collection.get()
        doc_names = set(m["source"] for m in all_docs["metadatas"])
        for name in doc_names:
            st.write(f"  📄 {name}")
    else:
        st.write("No documents indexed yet.")


# --- Build the graph ---
@st.cache_resource
def get_graph():
    return build_graph()

app = get_graph()


# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_logs_history" not in st.session_state:
    st.session_state.agent_logs_history = []


# Display chat history
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

        # Show agent logs for assistant messages
        if msg["role"] == "assistant" and i < len(st.session_state.agent_logs_history):
            logs = st.session_state.agent_logs_history[i]
            if logs:
                with st.expander("🤖 Agent Activity"):
                    for log in logs:
                        st.text(log)


# --- Chat Input ---
if prompt := st.chat_input("Ask me anything..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Run the graph
    with st.chat_message("assistant"):
        with st.spinner("Agents working..."):
            result = app.invoke({
                "query": prompt,
                "chat_history": [],
                "doc_results": [],
                "web_results": [],
                "agent_plan": [],
                "final_answer": "",
                "sources": [],
                "agent_logs": [],
            })

        # Display answer
        st.write(result["final_answer"])

        # Display agent logs
        if result["agent_logs"]:
            with st.expander("🤖 Agent Activity"):
                for log in result["agent_logs"]:
                    st.text(log)

        # Display sources
        if result["sources"]:
            with st.expander("📚 Sources"):
                for src in result["sources"]:
                    if src["type"] == "document":
                        st.write(f"📄 {src['source']} — Page {src['page']}")
                    elif src["type"] == "web":
                        st.write(f"🌐 [{src['title']}]({src['url']})")

    # Save to history
    st.session_state.messages.append({"role": "assistant", "content": result["final_answer"]})
    st.session_state.agent_logs_history.append(None)  # placeholder for user msg
    st.session_state.agent_logs_history.append(result["agent_logs"])