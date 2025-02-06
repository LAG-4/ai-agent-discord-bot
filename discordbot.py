import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from agno.tools.discord import DiscordTools
import discord
from discord.ext import commands, tasks

# Load environment variables
load_dotenv()

# Enable proper intents
intents = discord.Intents.default()
intents.messages = True  # Allow message reading
intents.guilds = True    # Allow access to guilds
intents.members = True   # Required for privileged intents

class HealthTrendsBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

        # ✅ Fix: Properly use DiscordTools
        self.trend_agent = Agent(
    tools=[
        DuckDuckGo(),
        lambda: DiscordTools(
            bot_token=os.getenv("DISCORD_BOT_TOKEN"),
            enable_messaging=True,
            enable_history=True
        )
    ],

            model=Groq(id="llama3-70b-8192"),
            instructions=[
                "Identify trending health/wellness topics",
                "Generate Instagram Reel/YouTube Short ideas",
                "Format responses with markdown",
                "Include 5 relevant hashtags per idea",
                "Add source links when available"
            ],
            markdown=True
        )

        # Start background task
        self.daily_report.start()

    @tasks.loop(hours=24)
    async def daily_report(self):
        """Automated daily trends report"""
        report_channel_id = 123456789012345678  # Replace with actual channel ID
        channel = self.get_channel(report_channel_id)

        if channel is None:
            print(f"ERROR: Could not find channel {report_channel_id}")
            return

        response = self.trend_agent.run("Generate daily health trends report")
        await channel.send(response[:2000])  # Discord message limit

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)

# ✅ Fix: Ensure the bot token is correctly loaded
bot_token = os.getenv("DISCORD_BOT_TOKEN")
if not bot_token:
    raise ValueError("ERROR: DISCORD_BOT_TOKEN is missing!")

bot = HealthTrendsBot()

@bot.command()
async def trends(ctx):
    """Get current health trends"""
    response = bot.trend_agent.run("List top 5 trending health topics")
    response_text = str(response)  # ✅ Convert response to string
    await ctx.send(response_text[:2000])  # ✅ Now it's safe to slice

@bot.command()
async def video_idea(ctx, *, topic: str):
    """Generate video content ideas"""
    response = bot.trend_agent.run(
        f"Create Instagram Reel script about {topic} including: "
        "1. Hook 2. Key points 3. CTA 4. Hashtags"
    )
    response_text = str(response)  # ✅ Convert response to string
    await ctx.send(response_text[:2000])  # ✅ Now it's safe to slice

if __name__ == "__main__":
    bot.run(bot_token)