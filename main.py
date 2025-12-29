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
MODEL = "HuggingFaceH4/zephyr-7b-beta"


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

last_reply = 0


def ai_reply(message):
    url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    prompt = f"""Reply in rude sarcastic Hinglish like a toxic Discord bot.
User: {message}
Bot:"""

    data = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.9
        },
        "options": {
            "wait_for_model": True
        }
    }

    try:
        res = requests.post(url, headers=headers, json=data, timeout=60)
        j = res.json()

        if isinstance(j, list) and "generated_text" in j[0]:
            return j[0]["generated_text"].split("Bot:")[-1].strip()

        if "error" in j:
            return f"HuggingFace bol raha: {j['error']} 😒"

        return "HF kuch ajeeb response de raha 😐"

    except Exception as e:
        return f"Exception: {str(e)} 😑"


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
