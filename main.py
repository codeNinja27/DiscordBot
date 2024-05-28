import discord
import os

intents = discord.Intents.default()

client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')


token = os.getenv("TOKEN")
if token is None:
  print(
      "Error: Environment variable 'TOKEN' not found. Please set it   with your Discord bot token.")
else:
  client.run(token)