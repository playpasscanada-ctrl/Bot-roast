import discord
import requests
import os
import time
from flask import Flask
from threading import Thread

# ========= KEEP ALIVE =========
app = Flask('')

@app.route('/')
def home():
    return "Discord Rude Bot Running!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    Thread(target=run).start()


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

CHANNEL_ID = 1257403231772872895
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

last_reply = 0


def ai_reply(message):
    url = "https://router.huggingface.co/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Reply like a rude sarcastic toxic Discord bot in Hinglish."
            },
            {
                "role": "user",
                "content": message
            }
        ],
        "temperature": 0.9,
        "max_tokens": 120
    }

    try:
        res = requests.post(url, headers=headers, json=data, timeout=50)
        j = res.json()

        return j["choices"][0]["message"]["content"]

    except Exception:
        return "Server slow hai bhai, thoda sabr rak 😑"


@client.event
async def on_ready():
    print("AI Rude Bot Online 😎")


@client.event
async def on_message(message):
    global last_reply

    if message.author == client.user:
        return

    if message.author.bot:
        return

    if message.channel.id != CHANNEL_ID:
        return

    if time.time() - last_reply < 5:
        return

    last_reply = time.time()

    reply = ai_reply(message.content)
    await message.channel.send(reply)


keep_alive()
client.run(DISCORD_TOKEN)
