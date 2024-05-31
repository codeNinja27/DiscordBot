import discord
import os
from discord import client
from dotenv import load_dotenv
from discord.ext import commands
import requests
import json
import random
from replit import db
# from keep_alive import keep_alive

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
    
##Insert encouragements into the database
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys(): ##checking if the key is in the database already
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]
    
##Deleting encouragements from the database
def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

intents = discord.Intents.default()  
intents.message_content = True
client = discord.Client(intents=intents)

onepiece_characters = ["Luffy", "Sanji", "Zoro", "Nami", "Usopp", "Chopper", "Robin", "Franky", "Brook", "Jinbe", "Ace", "Nico Robin", "Kid", "Law", "Kizaru", "Big Mom", "Shanks", "Blackbeard", "Buggy"]

sad_words = ["sad", "sadge", "depressed", "depressing", "unhappy", "angry", "miserable", "crying", "Depression", "cry", "joji"]

starter_encouragements = ["Cheer up!", "Hang in there!", "You are a great person/bot", "You are amazing!",  "It's just a simulation!", "Take it easy!", "You a like the sun!", "whoa...like you the best person i seen in my life"]


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

  options = starter_encouragements
  
  if "encouragements" in db.keys(): ##checking if the key is in the database already
    options = options + db["encouragements"].value

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

  #adding new messeges to the database
  if msg.startswith("$new"):
    if "encouragements" in db.keys():##checking if the key is in the database already
      encouraging_message = msg.split("$new ", 1)[1]
      update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  #deleting messeges from the database
  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():##checking if the key is in the database already
      index = int(msg.split("$del", 1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
      
  #showing encouragement messages of database + starter_encouragements
  if msg.startswith("$show"):
    await message.channel.send(options)
    
  #showing one piece character list 
  if msg.startswith("$char"):
    await message.channel.send(onepiece_characters)

  #get a random one piece character
  if msg.startswith("$onepiece"):
    await message.channel.send("You are " + random.choice(onepiece_characters) + "!")

token = os.getenv("TOKEN")
print(token)
if token is None:
  print(
      "Error: Environment variable 'TOKEN' not found. Please set it   with your Discord bot token."
  )
else:
  client.run(token)
