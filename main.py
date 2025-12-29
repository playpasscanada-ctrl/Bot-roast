import discord
import requests
import os
import time
from flask import Flask
from threading import Thread

# ========= KEEP ALIVE SERVER =========
app = Flask('')

@app.route('/')
def home():
    return "Discord Rude Bot is Running!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    Thread(target=run).start()

# ========= ENV TOKENS =========
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

CHANNEL_ID = 1257403231772872895   # <-- Tumhara channel ID
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

# ========= DISCORD CLIENT =========
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

last_reply = 0


def ai_reply(message):
    url = f"https://router.huggingface.co/{MODEL}"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    prompt = f"""You are a sarcastic rude discord bot that replies in Hinglish attitude style only.
User: {message}
Bot:"""

    data = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 120,
            "temperature": 0.9
        },
        "options": {
            "wait_for_model": True
        }
    }

    try:
        res = requests.post(url, headers=headers, json=data)
        j = res.json()

        if isinstance(j, list) and "generated_text" in j[0]:
            reply = j[0]["generated_text"].split("Bot:")[-1].strip()
            return reply

        if "error" in j:
            return f"HuggingFace bol raha: {j['error']} 😒"

        return "HF kuch ulta sidha de raha hai bhai 😐"

    except Exception:
        return "Server slow hai bhai, thoda sabr rak 😑"


@client.event
async def on_ready():
    print("AI Rude Bot Online 😎")
    print(f"Reply Only Channel => {CHANNEL_ID}")


@client.event
async def on_message(message):
    global last_reply

    if message.author == client.user:
        return

    if message.author.bot:
        return

    # Only that channel
    if message.channel.id != CHANNEL_ID:
        return

    # Cooldown — 5 sec
    if time.time() - last_reply < 5:
        return

    last_reply = time.time()

    reply = ai_reply(message.content)
    await message.channel.send(reply)


# ========= START =========
keep_alive()
client.run(DISCORD_TOKEN)
