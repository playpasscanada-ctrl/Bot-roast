import discord
import requests
import os
from keep_alive import keep_alive

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def ai_reply(message):
    url = f"https://api-inference.huggingface.co/models/{MODEL}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    prompt = f"Reply like a sarcastic rude discord bot in Hinglish. User: {message}\nBot:"

    data = {
        "inputs": prompt,
        "max_new_tokens": 100,
        "temperature": 0.9
    }

    res = requests.post(url, headers=headers, json=data)
    try:
        return res.json()[0]["generated_text"].split("Bot:")[-1].strip()
    except:
        return "Server slow hai bhai, shanti se baith 😒"

@client.event
async def on_ready():
    print("AI Rude Bot Online 😎")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.bot:
        return

    reply = ai_reply(message.content)
    await message.channel.send(reply)

keep_alive()
client.run(DISCORD_TOKEN)
