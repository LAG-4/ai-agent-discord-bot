import typer

from typing import Optional,List

from phi.model.groq import Groq

from phi.agent import Agent

from phi.storage.agent.postgres import PgAgentStorage

from phi.knowledge.pdf import PDFUrlKnowledgeBase

from phi.vectordb.pgvector import PgVector2

from phi.embedder.google import GeminiEmbedder



import os

from dotenv import load_dotenv



load_dotenv()





db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"





knowledge_base = PDFUrlKnowledgeBase(
    urls=[
        "https://image1121.s3.us-east-1.amazonaws.com/AryanGupta.pdf",
        "https://image1121.s3.us-east-1.amazonaws.com/kunal.pdf",
        "https://image1121.s3.us-east-1.amazonaws.com/ShivliRaina.pdf"
    ],
    vector_db=PgVector2(collection="reci", db_url=db_url, embedder=GeminiEmbedder())
)




knowledge_base.load()



storage=PgAgentStorage(table_name="pdf_assistant",db_url=db_url)



def pdf_assistant(new: bool = False, user: str = "user"):

    run_id: Optional[str] = None



    # if not new:

    #      existing_run_ids: List[str] = storage.get_all_run_ids(user)

    #      if len(existing_run_ids) > 0:

    #          run_id = existing_run_ids[0]



    assistant = Agent(

        model=Groq(id="llama-3.3-70b-versatile",embedder=GeminiEmbedder()),

        run_id=run_id,

        user_id=user,

        knowledge_base=knowledge_base,

        storage=storage,

        # Show tool calls in the response

        show_tool_calls=True,

        # Enable the assistant to search the knowledge base

        search_knowledge=True,

        # Enable the assistant to read the chat history

        read_chat_history=True,

    )

    if run_id is None:

        run_id = assistant.run_id

        print(f"Started Run: {run_id}\n")

    else:

        print(f"Continuing Run: {run_id}\n")



    assistant.cli_app(markdown=True)



if __name__=="__main__":

    typer.run(pdf_assistant)
