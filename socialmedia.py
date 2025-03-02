import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo

# Load environment variables
load_dotenv()

# Create the agent with updated instructions for plain text formatting
trend_agent = Agent(
    tools=[
        DuckDuckGo()
    ],
    model=Groq(id="llama3-70b-8192"),
    instructions=[
        "When a user inputs the name of a social media creator, search online for information about their YouTube channel.",
        "Analyze their video content to identify common patterns and topics they cover.",
        "List down the content creation patterns (such as posting frequency, style, recurring themes) and the main topics they focus on.",
        "Additionally, generate 2-3 similar video title ideas that the creator could use for their next videos.",
        "Then, choose one of those video title ideas and generate a detailed video script in the same style as that creator on that topic. The script should include an introduction, main points, and a conclusion.",
        "If the creator's content is predominantly in Hindi, generate the video script in Hindi; otherwise, generate the script in English.",
        "Format your response as plain text with clear section headings: 'Patterns', 'Topics', 'Video Title Ideas', and 'Video Script'.",
        "Include source links when available."
    ],
    markdown=False  # Disable markdown formatting
)

def main():
    print("Welcome to the Social Media Creator Analyzer (Terminal Interface)")
    print("Type 'exit' to quit.")
    while True:
        user_query = input("\nEnter a social media creator's name: ")
        if user_query.strip().lower() == "exit":
            break
        # Run the agent with the user query and print the response
        response = trend_agent.run(user_query)
        print("\nResponse:\n", response)

if __name__ == "__main__":
    main()
