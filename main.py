import discord
import os
from discord import client
from dotenv import load_dotenv
from discord.ext import commands
import requests
import json
import random

load_dotenv()

def get_quote():
  try:
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote
  except Exception as e:
    print(f"Error fetching quote: {e}")
    return "Could not fetch a quote at this time."

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

onepiece_characters = ["Luffy", "Sanji", "Zoro", "Nami", "Usopp", "Chopper", "Robin", "Franky", "Brook", "Jinbe", "Ace", "Nico Robin", "Kid", "Law", "Kizaru", "Big Mom", "Shanks", "Blackbeard", "Buggy"]

sad_words = ["sad", "sadge", "depressed", "depressing", "unhappy", "angry", "miserable"]

starter_encouragements = ["Cheer up!", "Hang in there", "You are a great person/bot", "You are amazing!",  "It's just a simulation", "Take it easy!", "Hang in there"]


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    print("Message from self")
    return
  msg = message.content
    
  if msg.startswith('$hello'):
    print("Message from $hello")
    await message.channel.send('Hello!')
    
  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))


token = os.getenv("TOKEN2")
print(token)
if token is None:
  print(
      "Error: Environment variable 'TOKEN' not found. Please set it   with your Discord bot token."
  )
else:
  client.run(token)
