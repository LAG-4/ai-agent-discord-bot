from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from textwrap import dedent
import os
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.exa import ExaTools

# Load environment variables and set API keys
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["EXA_API_KEY"] = os.getenv("EXA_API_KEY")

# Create FastAPI app
app = FastAPI()

# Initialize the Agno agent
agent = Agent(
    model=Groq(id="llama3-70b-8192"),
    tools=[
       ExaTools(
        include_domains=["cnbc.com", "reuters.com", "bloomberg.com"],
        category="news",
        text_length_limit=1000,
    )
    ],
    description="You are a distinguished research scholar with expertise in multiple disciplines.",
    instructions=dedent("""\
        - Conduct 3 distinct searches
        - Synthesize findings across sources
    """),
    expected_output=dedent("""\
        A professional research report in markdown format:

        # {Compelling Title That Captures the Topic's Essence}

        ## Introduction
        {Context and importance of the topic}

        ## Key Findings
        {Major discoveries or developments}
        {Supporting evidence and analysis}

        ## Key Takeaways
        - {Bullet point 1}
        - {Bullet point 2}
        - {Bullet point 3}

        ## Sources
        - [Source 1](link) - Key finding/quote
        - [Source 2](link) - Key finding/quote
        - [Source 3](link) - Key finding/quote

        ---
        Date: {current_date}
    """),
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
)

# Pydantic model for the request body
class Query(BaseModel):
    prompt: str

# POST endpoint to generate the research report
@app.post("/generate-report")
async def generate_report(query: Query):
    try:
        # Call the agent with the provided prompt.
        # This example uses a synchronous call to agent.run; adjust if your agent is asynchronous.
        result = agent.run(query.prompt)
        return {"report": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the application with uvicorn using an import string.
# Note: Make sure the filename is `main.py` so that "main:app" works as expected.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
