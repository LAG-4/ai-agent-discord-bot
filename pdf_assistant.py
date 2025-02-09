import streamlit as st
import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.storage.agent.postgres import PgAgentStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2
from phi.embedder.google import GeminiEmbedder

# Load environment variables
load_dotenv()

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="📄 AI-Powered PDF Assistant",
    page_icon="📑",
    layout="wide"
)

st.title("📄 AI PDF Assistant")
st.markdown("🚀 Upload PDF links, and let AI extract & summarize content!")

# ✅ Get Groq API Key from Streamlit secrets
groq_api_key = st.secrets["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = groq_api_key  # Make it globally available

# ✅ Database URL
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# ✅ User Input: Add PDF Links
st.sidebar.header("📂 Add PDF Links")
pdf_links = st.sidebar.text_area(
    "Enter PDF URLs (one per line):",
    placeholder="https://example.com/document1.pdf\nhttps://example.com/document2.pdf",
    height=150
).splitlines()

if pdf_links:
    st.sidebar.success(f"✅ Loaded {len(pdf_links)} PDFs!")

# ✅ Create Knowledge Base
def create_knowledge_base(pdf_links):
    if not pdf_links:
        return None
    return PDFUrlKnowledgeBase(
        urls=pdf_links,
        vector_db=PgVector2(collection="pdf_knowledge", db_url=db_url, embedder=GeminiEmbedder())
    )

# ✅ Load knowledge base
knowledge_base = create_knowledge_base(pdf_links)
if knowledge_base:
    try:
        knowledge_base.load()
        st.sidebar.success("📚 PDFs loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"⚠️ Error loading PDFs: {e}")

# ✅ Storage for Chat History
storage = PgAgentStorage(table_name="pdf_assistant", db_url=db_url)

# ✅ Initialize AI Assistant
@st.cache_resource
def initialize_agent():
    return Agent(
        model=Groq(id="llama-3.3-70b-versatile"),
        knowledge_base=knowledge_base,
        storage=storage,
        show_tool_calls=True,
        search_knowledge=True,
        read_chat_history=True,
    )

assistant = initialize_agent()

# ✅ User Input: Query AI
user_query = st.text_input("🔍 Ask a question about the PDFs", placeholder="What is the summary of document1?")
if st.button("🚀 Get Answer"):
    if not user_query:
        st.warning("Please enter a question!")
    elif not knowledge_base:
        st.error("No PDFs added! Please add some PDFs in the sidebar.")
    else:
        with st.spinner("Thinking... 🤔"):
            try:
                response = assistant.run(user_query)
                st.subheader("📝 AI Response")
                st.markdown(response.content)
            except Exception as e:
                st.error(f"⚠️ Error: {e}")

# --- Footer ---
st.markdown("---")
st.markdown("💡 Powered by AI Agents & Groq LLMs 🚀")
