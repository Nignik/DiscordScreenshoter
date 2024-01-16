import os
import discord
from dotenv import load_dotenv
from my_client import MyClient

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('CHANNEL')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents, CHANNEL)
client.run(TOKEN)