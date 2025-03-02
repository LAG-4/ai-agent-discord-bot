import streamlit as st
import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
# Streamlit Page Config
st.set_page_config(
    page_title="Finance & Web AI",
    page_icon="📈",
    layout="wide"
)

# --- Header ---
st.title("📈 AI-Powered Finance & Web Search Assistant")
st.markdown("🚀 Get real-time stock insights, analyst recommendations, and the latest news.")

# --- Define AI Agents ---

## Web Search Agent
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for the latest information",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tools_calls=True,
    markdown=True,
)

## Financial Agent
finance_agent = Agent(
    name="Finance AI Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[
        YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True),
    ],
    instructions=["Use tables to display the data"],
    show_tool_calls=True,
    markdown=True,
)

# Combined Multi-Agent System
multi_ai_agent = Agent(
    team=[finance_agent, web_search_agent],
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=[
        "Always include sources",
        "Use tables to display the data",
        "First use the Finance Agent to get stock data",
        "Then use the Web Search Agent for recent news",
    ],
    show_tools_calls=True,
    markdown=True,
)

<<<<<<< HEAD
multi_ai_agent.print_response("Summarize analyst recommendation and share the latest news for NVDA",stream=True)
x
=======
# --- Streamlit UI ---
st.sidebar.header("🔍 Search Options")
stock_symbol = st.sidebar.text_input("Enter Stock Ticker (e.g., NVDA, AAPL)", value="NVDA")
query_type = st.sidebar.selectbox(
    "Select Analysis Type",
    ["Stock Insights & Analyst Recommendations", "Latest News"],
)

if st.sidebar.button("🚀 Get Insights"):
    with st.spinner("Fetching AI-powered insights... ⏳"):
        try:
            if query_type == "Stock Insights & Analyst Recommendations":
                prompt = f"Summarize analyst recommendation and share the latest stock insights for {stock_symbol}"
            else:
                prompt = f"Find the latest news about {stock_symbol}"

            response = multi_ai_agent.run(prompt)

            # Display results
            st.subheader("📝 AI-Generated Insights")
            st.markdown(response.content)

        except Exception as e:
            st.error(f"⚠️ Error fetching insights: {e}")

# --- Footer ---
st.markdown("---")
st.markdown("🔗 Powered by AI Agents & Groq LLMs")

>>>>>>> 8c1fd3725a71070c3fbb662d575bad73fc9101b5
