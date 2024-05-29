from typing import Tuple
import discord
import os
from discord import client
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
# intents.message_content = True
client = discord.Client(intents=intents)
# client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    print("Message from self")
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')


token = os.getenv("TOKEN2")
print(token)
if token is None:
  print(
      "Error: Environment variable 'TOKEN' not found. Please set it   with your Discord bot token."
  )
else:
  client.run(token)
