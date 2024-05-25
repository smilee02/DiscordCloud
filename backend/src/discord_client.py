import os
import discord
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Initialize Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def load_discord():
    loop = asyncio.get_event_loop()
    await client.login(DISCORD_TOKEN)
    loop.create_task(client.connect())
    
def get_client():
    return client