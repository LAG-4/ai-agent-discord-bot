import typer
from typing import Optional, List
import os
from dotenv import load_dotenv

from phi.model.groq import Groq
from phi.agent import Agent
from phi.storage.agent.postgres import PgAgentStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2
from phi.embedder.google import GeminiEmbedder

# ✅ Load environment variables
load_dotenv()

# ✅ Retrieve API Key from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ✅ Database connection URL
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# ✅ Initialize PDF Knowledge Base
knowledge_base = PDFUrlKnowledgeBase(
    urls=[
        "https://image1121.s3.us-east-1.amazonaws.com/AdityaMayank.pdf",
        "https://image1121.s3.us-east-1.amazonaws.com/AryanGupta.pdf",
        "https://image1121.s3.us-east-1.amazonaws.com/ShivliRaina.pdf",
    ],
    vector_db=PgVector2(collection="reci", db_url=db_url, embedder=GeminiEmbedder()),
)

# ✅ Load knowledge base
try:
    knowledge_base.load()
except Exception as e:
    print(f"⚠️ Error loading knowledge base: {e}")

# ✅ Initialize storage
storage = PgAgentStorage(table_name="pdf_assistant", db_url=db_url)

def pdf_assistant(new: bool = False, user: str = "user"):
    run_id: Optional[str] = None

    # ✅ Ensure API Key is set
    if not GROQ_API_KEY:
        print("🚨 GROQ_API_KEY is missing! Please add it to your .env file.")
        return

    # ✅ Initialize Assistant
    assistant = Agent(
        model=Groq(id="llama-3.3-70b-versatile", api_key=GROQ_API_KEY, embedder=GeminiEmbedder()),
        run_id=run_id,
        user_id=user,
        knowledge_base=knowledge_base,
        storage=storage,
        show_tool_calls=True,   # ✅ Show tool calls in response
        search_knowledge=True,  # ✅ Enable knowledge base search
        read_chat_history=True, # ✅ Enable chat history
    )

    # ✅ Print Run ID
    if run_id is None:
        run_id = assistant.run_id
        print(f"✅ Started Run: {run_id}\n")
    else:
        print(f"✅ Continuing Run: {run_id}\n")

    # ✅ Start CLI App
    assistant.cli_app(markdown=True)

if __name__ == "__main__":
    typer.run(pdf_assistant)
