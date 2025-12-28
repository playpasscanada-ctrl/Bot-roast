import discord
import requests
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def ai_reply(message):
    url = f"https://api-inference.huggingface.co/models/{MODEL}"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    prompt = f"""You are a sarcastic rude discord bot that replies in Hinglish attitude style.
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

        # SUCCESS
        if isinstance(j, list) and "generated_text" in j[0]:
            reply = j[0]["generated_text"].split("Bot:")[-1].strip()
            return reply

        # HF Returning Error
        if "error" in j:
            return f"HuggingFace bol raha: {j['error']} 😒"

        return "Bhai HF kuch ulta seedha de raha hai 😐"

    except Exception as e:
        return "Server slow hai bhai, shanti se baith 😑"


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


client.run(DISCORD_TOKEN)
